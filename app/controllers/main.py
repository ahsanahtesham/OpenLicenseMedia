from flask import Blueprint, render_template
from flask_login import current_user
from datetime import datetime

# Create a blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def index():
    return render_template('main/index.html', title='Home')

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='About') 