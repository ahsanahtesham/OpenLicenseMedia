import unittest
from unittest.mock import patch, MagicMock
from app.services.openverse_api import OpenverseAPI

class TestOpenverseAPI(unittest.TestCase):
    def setUp(self):
        self.api = OpenverseAPI()
    
    @patch('app.services.openverse_api.requests.Session')
    def test_search_images(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result_count': 2,
            'results': [
                {
                    'id': 'img1',
                    'title': 'Test Image 1',
                    'creator': 'Test Creator',
                    'source': 'test_source',
                    'license': 'CC0',
                    'url': 'https://example.com/img1.jpg',
                    'thumbnail': 'https://example.com/img1_thumb.jpg'
                },
                {
                    'id': 'img2',
                    'title': 'Test Image 2',
                    'creator': 'Test Creator',
                    'source': 'test_source',
                    'license': 'CC BY',
                    'url': 'https://example.com/img2.jpg',
                    'thumbnail': 'https://example.com/img2_thumb.jpg'
                }
            ]
        }
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        result = self.api.search_images('test', license='CC0')
        
        # Assert the method was called correctly
        mock_session.return_value.get.assert_called_once()
        args, kwargs = mock_session.return_value.get.call_args
        self.assertEqual(kwargs['params']['q'], 'test')
        self.assertEqual(kwargs['params']['license'], 'CC0')
        
        # Assert the result is processed correctly
        self.assertEqual(result['result_count'], 2)
        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['results'][0]['title'], 'Test Image 1')
    
    @patch('app.services.openverse_api.requests.Session')
    def test_search_audio(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result_count': 1,
            'results': [
                {
                    'id': 'audio1',
                    'title': 'Test Audio',
                    'creator': 'Test Creator',
                    'source': 'test_source',
                    'license': 'CC BY',
                    'url': 'https://example.com/audio1.mp3'
                }
            ]
        }
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        result = self.api.search_audio('test')
        
        # Assert the method was called correctly
        mock_session.return_value.get.assert_called_once()
        
        # Assert the result is processed correctly
        self.assertEqual(result['result_count'], 1)
        self.assertEqual(result['results'][0]['title'], 'Test Audio')
    
    @patch('app.services.openverse_api.requests.Session')
    def test_get_image_detail(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 'img1',
            'title': 'Test Image Detail',
            'creator': 'Test Creator',
            'source': 'test_source',
            'license': 'CC0',
            'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'url': 'https://example.com/img1.jpg',
            'thumbnail': 'https://example.com/img1_thumb.jpg',
            'tags': ['nature', 'sky', 'mountain'],
            'description': 'Test description',
            'date_created': '2022-01-01T00:00:00Z'
        }
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        result = self.api.get_image_detail('img1')
        
        # Assert the method was called correctly
        mock_session.return_value.get.assert_called_once()
        
        # Assert the result is processed correctly
        self.assertEqual(result['id'], 'img1')
        self.assertEqual(result['title'], 'Test Image Detail')
        self.assertEqual(len(result['tags']), 3)
    
    @patch('app.services.openverse_api.requests.Session')
    def test_get_licenses(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'id': 'CC0', 'name': 'CC0 1.0 Universal'},
            {'id': 'CC-BY', 'name': 'Attribution 4.0 International'},
            {'id': 'CC-BY-SA', 'name': 'Attribution-ShareAlike 4.0 International'}
        ]
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        result = self.api.get_licenses()
        
        # Assert the method was called correctly
        mock_session.return_value.get.assert_called_once()
        
        # Assert the result is processed correctly
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['id'], 'CC0')
        self.assertEqual(result[1]['name'], 'Attribution 4.0 International')

if __name__ == '__main__':
    unittest.main() 