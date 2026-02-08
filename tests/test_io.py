"""
Tests for additionals.io module
"""
import unittest
from unittest.mock import Mock, patch
import os
import tempfile

from additionals.io import relativepath, abspath, basename, dirname, path_exists, listdir


class TestIOFilters(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.mock_ctx = Mock()
        self.mock_ctx.name = "/path/to/template.j2"
        
        # Temporary directory and file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.temp_file, "w") as f:
            f.write("test content")
    
    def tearDown(self):
        """Cleanup after testing"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_relativepath(self):
        """relativepath filter test"""
        # Set name attribute of mock context
        self.mock_ctx.name = "/home/user/project/templates/template.j2"
        
        # Resolve relative path
        result = relativepath(self.mock_ctx, "../data/file.txt")
        expected = os.path.normpath("/home/user/project/data/file.txt")
        self.assertEqual(result, expected)
        
        # File in current directory
        result = relativepath(self.mock_ctx, "config.yaml")
        expected = os.path.normpath("/home/user/project/templates/config.yaml")
        self.assertEqual(result, expected)
    
    def test_abspath(self):
        """abspath filter test"""
        # Absolute path (as is)
        result = abspath(self.mock_ctx, "/home/user/file.txt")
        self.assertEqual(result, "/home/user/file.txt")
        
        # Relative path (converted to absolute)
        result = abspath(self.mock_ctx, "file.txt")
        expected = os.path.abspath("file.txt")
        self.assertEqual(result, expected)
        
        # Non-string input (converted with str())
        result = abspath(self.mock_ctx, 123)
        expected = os.path.abspath("123")
        self.assertEqual(result, expected)
    
    def test_basename(self):
        """basename filter test"""
        # Normal file path
        result = basename(self.mock_ctx, "/path/to/file.txt")
        self.assertEqual(result, "file.txt")
        
        # Directory path (no trailing slash)
        result = basename(self.mock_ctx, "/path/to/directory")
        self.assertEqual(result, "directory")
        
        # Directory path (with trailing slash)
        result = basename(self.mock_ctx, "/path/to/directory/")
        self.assertEqual(result, "")
        
        # Root path
        result = basename(self.mock_ctx, "/")
        self.assertEqual(result, "")
        
        # Filename only
        result = basename(self.mock_ctx, "file.txt")
        self.assertEqual(result, "file.txt")
        
        # Non-string input
        result = basename(self.mock_ctx, 123)
        expected = os.path.basename("123")
        self.assertEqual(result, expected)
    
    def test_dirname(self):
        """dirname filter test"""
        # Normal file path
        result = dirname(self.mock_ctx, "/path/to/file.txt")
        self.assertEqual(result, "/path/to")
        
        # Directory path
        result = dirname(self.mock_ctx, "/path/to/directory")
        self.assertEqual(result, "/path/to")
        
        # File in root directory
        result = dirname(self.mock_ctx, "/file.txt")
        self.assertEqual(result, "/")
        
        # Root path
        result = dirname(self.mock_ctx, "/")
        self.assertEqual(result, "/")
        
        # Filename only
        result = dirname(self.mock_ctx, "file.txt")
        self.assertEqual(result, "")
        
        # Non-string input
        result = dirname(self.mock_ctx, 123)
        expected = os.path.dirname("123")
        self.assertEqual(result, expected)
    
    def test_path_exists(self):
        """path_exists filter test"""
        # Existing file
        result = path_exists(self.mock_ctx, self.temp_file)
        self.assertTrue(result)
        
        # Existing directory
        result = path_exists(self.mock_ctx, self.temp_dir)
        self.assertTrue(result)
        
        # Non-existent file
        result = path_exists(self.mock_ctx, "/nonexistent/file.txt")
        self.assertFalse(result)
        
        # Non-existent directory
        result = path_exists(self.mock_ctx, "/nonexistent/directory")
        self.assertFalse(result)
        
        # Non-string input
        result = path_exists(self.mock_ctx, 123)
        expected = os.path.exists("123")
        self.assertEqual(result, expected)
    
    def test_listdir(self):
        """listdir filter test"""
        # Real directory
        result = listdir(self.mock_ctx, self.temp_dir)
        self.assertIsInstance(result, list)
        self.assertIn("test_file.txt", result)
        
        # Empty directory
        empty_dir = os.path.join(self.temp_dir, "empty")
        os.makedirs(empty_dir)
        result = listdir(self.mock_ctx, empty_dir)
        self.assertEqual(result, [])
        
        # Non-existent directory (should raise exception)
        with self.assertRaises(OSError):
            listdir(self.mock_ctx, "/nonexistent/directory")
        
        # Non-string input
        result = listdir(self.mock_ctx, self.temp_dir)  # expecting pathlib.Path object etc.
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
