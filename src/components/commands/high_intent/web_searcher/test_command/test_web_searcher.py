import unittest
from unittest.mock import patch
from src.components.commands.web_searcher.web_searcher import WebSearcher

class TestWebSearcher(unittest.TestCase):
    """Class for testing the WebSearcher command"""
    
    def setUp(self):
        self.web_searcher = WebSearcher()
        
    @patch('webbrowser.open')
    def test_open_website(self, mock_open):
        website_query = "google"
        response = self.web_searcher.open_website(website_query)
        mock_open.assert_called_once_with(f"https://www.{website_query}.com")
        self.assertEqual(response, f'Opening {website_query}.com')

    @patch('webbrowser.open')
    def test_search_google(self, mock_open):
        google_query = "cats"
        response = self.web_searcher.search_google(google_query)
        mock_open.assert_called_once_with(f"https://www.google.com/search?q={google_query}")
        self.assertEqual(response, f'Searching google for {google_query}')
    
    @patch('webbrowser.open')
    def test_search_youtube(self, mock_open):
        youtube_query = "cats"
        response = self.web_searcher.search_youtube(youtube_query)
        mock_open.assert_called_once_with(f"https://www.youtube.com/results?search_query={youtube_query}")
        self.assertEqual(response, f'Searching youtube for {youtube_query}')
        
if __name__ == '__main__':
    unittest.main()
