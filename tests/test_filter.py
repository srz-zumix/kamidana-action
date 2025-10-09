"""
Tests for additionals.filter module
"""
import unittest
from unittest.mock import Mock
import base64
import re

from additionals.filter import regex_replace, ternary, b64encode


class TestFilterFilters(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.mock_ctx = Mock()
        self.mock_ctx.name = "test_template.j2"
    
    def test_regex_replace_basic(self):
        """regex_replace filter basic functionality test"""
        # Simple replacement
        result = regex_replace(self.mock_ctx, "hello world", "world", "python")
        self.assertEqual(result, "hello python")
        
        # Regular expression pattern
        result = regex_replace(self.mock_ctx, "abc123def", r"\d+", "XXX")
        self.assertEqual(result, "abcXXXdef")
        
        # Replace all matches (count=0 for all)
        result = regex_replace(self.mock_ctx, "a1b2c3", r"\d", "X")
        self.assertEqual(result, "aXbXcX")
        
        # Replace only the first one (count=1)
        result = regex_replace(self.mock_ctx, "a1b2c3", r"\d", "X", count=1)
        self.assertEqual(result, "aXb2c3")
    
    def test_regex_replace_flags(self):
        """regex_replace filter flags test"""
        # Case-insensitive replacement
        result = regex_replace(self.mock_ctx, "Hello World", "hello", "hi", flags=re.IGNORECASE)
        self.assertEqual(result, "hi World")
        
        # Multiline support
        text = "line1\nline2"
        result = regex_replace(self.mock_ctx, text, r"^line", "LINE", flags=re.MULTILINE)
        self.assertEqual(result, "LINE1\nLINE2")
    
    def test_ternary_basic(self):
        """ternary filter basic functionality test"""
        # When True
        result = ternary(self.mock_ctx, True, "yes", "no")
        self.assertEqual(result, "yes")
        
        # When False
        result = ternary(self.mock_ctx, False, "yes", "no")
        self.assertEqual(result, "no")
        
        # When 0 (Falsy)
        result = ternary(self.mock_ctx, 0, "yes", "no")
        self.assertEqual(result, "no")
        
        # When empty string (Falsy)
        result = ternary(self.mock_ctx, "", "yes", "no")
        self.assertEqual(result, "no")
        
        # When non-empty string (Truthy)
        result = ternary(self.mock_ctx, "hello", "yes", "no")
        self.assertEqual(result, "yes")
        
        # When empty list (Falsy)
        result = ternary(self.mock_ctx, [], "yes", "no")
        self.assertEqual(result, "no")
        
        # When non-empty list (Truthy)
        result = ternary(self.mock_ctx, [1], "yes", "no")
        self.assertEqual(result, "yes")
    
    def test_ternary_with_null_val(self):
        """ternary filter null_val option test"""
        # null_val is used when None
        result = ternary(self.mock_ctx, None, "yes", "no", "null")
        self.assertEqual(result, "null")
        
        # When False, false_val is used (not null_val)
        result = ternary(self.mock_ctx, False, "yes", "no", "null")
        self.assertEqual(result, "no")
        
        # When null_val is not specified, false_val is used even for None
        result = ternary(self.mock_ctx, None, "yes", "no")
        self.assertEqual(result, "no")
    
    def test_b64encode_basic(self):
        """b64encode filter basic functionality test"""
        # Normal string
        result = b64encode(self.mock_ctx, "hello")
        expected = base64.b64encode("hello".encode('utf-8'))
        self.assertEqual(result, expected)
        
        # Empty string
        result = b64encode(self.mock_ctx, "")
        expected = base64.b64encode("".encode('utf-8'))
        self.assertEqual(result, expected)
        
        # String with special characters
        result = b64encode(self.mock_ctx, "hello\nworld")
        expected = base64.b64encode("hello\nworld".encode('utf-8'))
        self.assertEqual(result, expected)
    
    def test_b64encode_encoding(self):
        """b64encode filter encoding test"""
        # UTF-8 encoding (default)
        result = b64encode(self.mock_ctx, "hello world")
        expected = base64.b64encode("hello world".encode('utf-8'))
        self.assertEqual(result, expected)
        
        # Explicitly specify UTF-8
        result = b64encode(self.mock_ctx, "hello world", encoding='utf-8')
        expected = base64.b64encode("hello world".encode('utf-8'))
        self.assertEqual(result, expected)
        
        # ASCII encoding
        result = b64encode(self.mock_ctx, "hello", encoding='ascii')
        expected = base64.b64encode("hello".encode('ascii'))
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
