// Main JavaScript for Open License Media Search

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Media type dropdown change handler for search form
    const mediaTypeSelect = document.getElementById('media_type');
    if (mediaTypeSelect) {
        mediaTypeSelect.addEventListener('change', function() {
            updateSourceDropdown(this.value);
        });
        
        // Initialize source dropdown based on current media type
        updateSourceDropdown(mediaTypeSelect.value);
    }

    // Function to update source dropdown based on media type
    function updateSourceDropdown(mediaType) {
        const sourceSelect = document.getElementById('source');
        if (!sourceSelect) return;
        
        // Clear current options
        sourceSelect.innerHTML = '<option value="">All Sources</option>';
        
        // Add options based on media type (can be expanded with real data)
        if (mediaType === 'images') {
            addOption(sourceSelect, 'flickr', 'Flickr');
            addOption(sourceSelect, 'wikimedia', 'Wikimedia');
            addOption(sourceSelect, 'rawpixel', 'Rawpixel');
        } else if (mediaType === 'audio') {
            addOption(sourceSelect, 'jamendo', 'Jamendo');
            addOption(sourceSelect, 'ccmixter', 'ccMixter');
            addOption(sourceSelect, 'freesound', 'Freesound');
        }
    }

    // Helper function to add options to select
    function addOption(select, value, text) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        select.appendChild(option);
    }

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}); 