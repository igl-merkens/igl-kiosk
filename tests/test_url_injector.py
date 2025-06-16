# tests/test_url_injector.py
"""Tests for URL injector functionality."""

import json
import tempfile
#import time
import unittest
from pathlib import Path
#from unittest.mock import patch, MagicMock

from PyQt6.QtCore import QCoreApplication
from PyQt6.QtTest import QSignalSpy

from igl_kiosk.core.url_injector import URLInjector


class TestURLInjector(unittest.TestCase):
    """Test cases for URLInjector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QCoreApplication.instance()
        if self.app is None:
            self.app = QCoreApplication([])
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
        
        self.injector = URLInjector(str(self.temp_path))
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.injector.stop_monitoring()
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_create_command_file(self):
        """Test command file creation."""
        # Remove the file if it exists
        if self.temp_path.exists():
            self.temp_path.unlink()
        
        # Create new injector which should create the file
        injector = URLInjector(str(self.temp_path))
        
        self.assertTrue(self.temp_path.exists())
        
        with open(self.temp_path, 'r') as f:
            data = json.load(f)
        
        self.assertIn('instructions', data)
        self.assertIn('url', data)
        self.assertEqual(data['url'], '')
    
    def test_url_signal_emission(self):
        """Test that URL changes emit signals."""
        spy = QSignalSpy(self.injector.url_received)
        
        # Write URL to command file
        test_url = "https://example.com"
        with open(self.temp_path, 'w') as f:
            json.dump({"url": test_url}, f)
        
        # Process the file change
        self.injector._process_command_file()
        
        # Check that signal was emitted
        self.assertEqual(len(spy), 1)
        self.assertEqual(spy[0][0], test_url)
    
    def test_empty_url_ignored(self):
        """Test that empty URLs are ignored."""
        spy = QSignalSpy(self.injector.url_received)
        
        # Write empty URL to command file
        with open(self.temp_path, 'w') as f:
            json.dump({"url": ""}, f)
        
        self.injector._process_command_file()
        
        # Check that no signal was emitted
        self.assertEqual(len(spy), 0)
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON."""
        # Write invalid JSON
        with open(self.temp_path, 'w') as f:
            f.write("invalid json")
        
        # Should not raise exception
        try:
            self.injector._process_command_file()
        except Exception as e:
            self.fail(f"Processing invalid JSON raised an exception: {e}")

