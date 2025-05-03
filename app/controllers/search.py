from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models.user import Search
from app.forms import SearchForm
from app.services.openverse_api import OpenverseAPI
from datetime import datetime

# Create a blueprint for search routes
search_bp = Blueprint('search', __name__)
openverse_api = OpenverseAPI()

# Default licenses to use if API fails
DEFAULT_LICENSES = [
    ('', 'All Licenses'),
    ('cc0', 'CC0'),
    ('by', 'CC BY'),
    ('by-sa', 'CC BY-SA'),
    ('by-nc', 'CC BY-NC'),
    ('by-nd', 'CC BY-ND'),
    ('by-nc-sa', 'CC BY-NC-SA'),
    ('by-nc-nd', 'CC BY-NC-ND')
]

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    
    # Dynamically populate the license and source choices
    try:
        licenses = openverse_api.get_licenses()
        license_choices = [('', 'All Licenses')] + [(license['id'], license['name']) for license in licenses]
        form.license.choices = license_choices
    except Exception as e:
        # Use default licenses if API fails
        form.license.choices = DEFAULT_LICENSES
        flash(f"Using default license options. API error: {str(e)}", 'warning')
    
    # Always populate source choices
    form.source.choices = [('', 'All Sources')]
    if form.media_type.data == 'images':
        form.source.choices += [
            ('flickr', 'Flickr'),
            ('wikimedia', 'Wikimedia'),
            ('rawpixel', 'Rawpixel')
        ]
    else:  # audio
        form.source.choices += [
            ('jamendo', 'Jamendo'),
            ('ccmixter', 'ccMixter'),
            ('freesound', 'Freesound')
        ]
    
    results = None
    page = request.args.get('page', 1, type=int)
    
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data or request.args.get('query')
        media_type = form.media_type.data or request.args.get('media_type', 'images')
        license = form.license.data or request.args.get('license', None)
        source = form.source.data or request.args.get('source', None)
        
        # Save search to history if user is logged in
        if current_user.is_authenticated:
            search_record = Search(
                query=query,
                media_type=media_type,
                user_id=current_user.id
            )
            db.session.add(search_record)
            db.session.commit()
        
        # Perform the search based on media type
        try:
            if media_type == 'images':
                results = openverse_api.search_images(
                    query=query, 
                    page=page, 
                    license=license, 
                    source=source
                )
            elif media_type == 'audio':
                results = openverse_api.search_audio(
                    query=query, 
                    page=page, 
                    license=license, 
                    source=source
                )
                
            # Update form with search parameters
            form.query.data = query
            form.media_type.data = media_type
            form.license.data = license
            form.source.data = source
            
            # Check if results were returned
            if not results or 'results' not in results or not results['results']:
                flash(f"No results found for '{query}'. Try different search terms or filters.", 'info')
            
        except Exception as e:
            flash(f"Error performing search: {str(e)}", 'danger')
    
    return render_template(
        'search/search.html', 
        title='Search', 
        form=form, 
        results=results, 
        page=page,
        query=form.query.data
    )

@search_bp.route('/detail/<string:media_type>/<string:media_id>')
def detail(media_type, media_id):
    try:
        if media_type == 'images':
            details = openverse_api.get_image_detail(media_id)
        elif media_type == 'audio':
            details = openverse_api.get_audio_detail(media_id)
        else:
            flash('Invalid media type', 'danger')
            return redirect(url_for('search.search'))
    except Exception as e:
        flash(f"Error retrieving details: {str(e)}", 'danger')
        return redirect(url_for('search.search'))
        
    return render_template(
        'search/detail.html',
        title='Media Details',
        details=details,
        media_type=media_type
    )

@search_bp.route('/history')
@login_required
def search_history():
    searches = db.session.query(Search).filter_by(user_id=current_user.id).order_by(Search.search_time.desc()).all()
    return render_template('search/history.html', title='Search History', searches=searches)

@search_bp.route('/history/delete/<int:search_id>', methods=['POST'])
@login_required
def delete_search(search_id):
    search = db.session.query(Search).get_or_404(search_id)
    
    # Check if the search belongs to the current user
    if search.user_id != current_user.id:
        flash('You do not have permission to delete this search.', 'danger')
        return redirect(url_for('search.search_history'))
    
    db.session.delete(search)
    db.session.commit()
    flash('Search record deleted.', 'success')
    return redirect(url_for('search.search_history')) 