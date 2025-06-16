"""Tests for browser functionality."""

import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import QCoreApplication

from igl_kiosk.core.browser import BackgroundLoader, URLHandler


class TestURLHandler(unittest.TestCase):
    """Test cases for URLHandler class."""
    
    def test_normalize_url_with_protocol(self):
        """Test URL normalization with existing protocol."""
        url = "https://example.com"
        normalized = URLHandler.normalize_url(url)
        self.assertEqual(normalized, "https://example.com")
    
    def test_normalize_url_without_protocol(self):
        """Test URL normalization without protocol."""
        url = "example.com"
        normalized = URLHandler.normalize_url(url)
        self.assertEqual(normalized, "https://example.com")
    
    def test_normalize_empty_url(self):
        """Test normalization of empty URL."""
        normalized = URLHandler.normalize_url("")
        self.assertEqual(normalized, "")
        
        normalized = URLHandler.normalize_url("   ")
        self.assertEqual(normalized, "")
    
    def test_is_valid_url(self):
        """Test URL validation."""
        self.assertTrue(URLHandler.is_valid_url("example.com"))
        self.assertTrue(URLHandler.is_valid_url("https://example.com"))
        self.assertFalse(URLHandler.is_valid_url(""))
        self.assertFalse(URLHandler.is_valid_url("invalid"))


class TestBackgroundLoader(unittest.TestCase):
    """Test cases for BackgroundLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QCoreApplication.instance()
        if self.app is None:
            self.app = QCoreApplication([])
        
        self.loader = BackgroundLoader()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.loader.cleanup()
    
    @patch('igl_kiosk.core.browser.QWebEngineView')
    def test_load_url(self, mock_web_view):
        """Test URL loading."""
        mock_view = MagicMock()
        mock_web_view.return_value = mock_view
        
        test_url = "example.com"
        web_view = self.loader.load_url(test_url)
        
        # Should normalize URL and set it
        mock_view.setUrl.assert_called_once()
        # Should connect load finished signal
        mock_view.loadFinished.connect.assert_called_once()
    
    def test_cleanup(self):
        """Test cleanup functionality."""
        # Add mock views to loading_views
        mock_view1 = MagicMock()
        mock_view2 = MagicMock()
        self.loader.loading_views = [mock_view1, mock_view2]
        
        self.loader.cleanup()
        
        # Should call deleteLater on all views
        mock_view1.deleteLater.assert_called_once()
        mock_view2.deleteLater.assert_called_once()
        # Should clear the list
        self.assertEqual(len(self.loader.loading_views), 0)


if __name__ == '__main__':
    unittest.main()