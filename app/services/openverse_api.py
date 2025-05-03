import requests
from urllib.parse import urljoin
import logging

class OpenverseAPI:
    BASE_URL = "https://api.openverse.org/v1/"
    
    def __init__(self):
        self.session = requests.Session()
        # Add a user-agent to identify our application to the API
        self.session.headers.update({
            'User-Agent': 'OpenLicenseMediaSearch/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint, params=None, timeout=10):
        """
        Makes a request to the Openverse API with error handling
        
        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            timeout (int): Request timeout in seconds
            
        Returns:
            dict: Response data as JSON
            
        Raises:
            Exception: If request fails
        """
        try:
            url = urljoin(self.BASE_URL, endpoint)
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise Exception(f"API request failed: {e}")
        
    def search_images(self, query, page=1, page_size=20, license=None, source=None):
        """
        Search for images on Openverse
        
        Args:
            query (str): Search query
            page (int): Page number for pagination
            page_size (int): Number of results per page
            license (str, optional): Filter by license type
            source (str, optional): Filter by source
            
        Returns:
            dict: Search results
        """
        endpoint = "images/"
        params = {
            "q": query,
            "page": page,
            "page_size": page_size
        }
        
        if license and license != '':
            params["license"] = license
        if source and source != '':
            params["source"] = source
            
        return self._make_request(endpoint, params)
    
    def search_audio(self, query, page=1, page_size=20, license=None, source=None):
        """
        Search for audio on Openverse
        
        Args:
            query (str): Search query
            page (int): Page number for pagination
            page_size (int): Number of results per page
            license (str, optional): Filter by license type
            source (str, optional): Filter by source
            
        Returns:
            dict: Search results
        """
        endpoint = "audio/"
        params = {
            "q": query,
            "page": page,
            "page_size": page_size
        }
        
        if license and license != '':
            params["license"] = license
        if source and source != '':
            params["source"] = source
            
        return self._make_request(endpoint, params)
    
    def get_image_detail(self, image_id):
        """
        Get details for a specific image
        
        Args:
            image_id (str): Image ID
            
        Returns:
            dict: Image details
        """
        endpoint = f"images/{image_id}/"
        return self._make_request(endpoint)
    
    def get_audio_detail(self, audio_id):
        """
        Get details for a specific audio file
        
        Args:
            audio_id (str): Audio ID
            
        Returns:
            dict: Audio details
        """
        endpoint = f"audio/{audio_id}/"
        return self._make_request(endpoint)
    
    def get_sources(self, media_type):
        """
        Get available sources for the media type
        
        Args:
            media_type (str): Either 'images' or 'audio'
            
        Returns:
            list: Available sources
        """
        endpoint = f"{media_type}/stats/"
        return self._make_request(endpoint)
        
    def get_licenses(self):
        """
        Get available licenses
        
        Returns:
            list: Available licenses or empty list if endpoint not found
        """
        try:
            endpoint = "licenses/"
            return self._make_request(endpoint)
        except Exception:
            # The licenses endpoint might have changed or been removed
            # Return an empty list to handle gracefully
            return [] 