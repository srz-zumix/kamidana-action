"""
Tests for additionals.json module
"""
import unittest
from unittest.mock import Mock, patch
import json
from jinja2 import Environment

# Import filters to test
from additionals.json import json_query, json_dumps, json_loads, json_escape


class TestJsonFilters(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.env = Environment()
        self.mock_ctx = Mock()
        self.mock_ctx.name = "test_template.j2"
    
    def test_json_query_basic(self):
        """Test json_query filter basic functionality"""
        data = {"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}
        
        # Simple query
        result = json_query(self.mock_ctx, data, "users[0].name")
        self.assertEqual(result, "Alice")
        
        # Array length
        result = json_query(self.mock_ctx, data, "length(users)")
        self.assertEqual(result, 2)
        
        # Non-existent path
        result = json_query(self.mock_ctx, data, "nonexistent")
        self.assertIsNone(result)
    
    def test_json_dumps_basic(self):
        """Test json_dumps filter basic functionality"""
        # String
        result = json_dumps(self.mock_ctx, "hello")
        self.assertEqual(result, '"hello"')
        
        # Number
        result = json_dumps(self.mock_ctx, 123)
        self.assertEqual(result, '123')
        
        # Array
        result = json_dumps(self.mock_ctx, [1, 2, 3])
        self.assertEqual(result, '[1, 2, 3]')
        
        # Object
        result = json_dumps(self.mock_ctx, {"key": "value"})
        self.assertEqual(result, '{"key": "value"}')
    
    def test_json_dumps_options(self):
        """json_dumps filter options test"""
        data = {"b": 2, "a": 1}
        
        # sort_keys option
        result = json_dumps(self.mock_ctx, data, sort_keys=True)
        self.assertEqual(result, '{"a": 1, "b": 2}')
        
        # indent option
        result = json_dumps(self.mock_ctx, data, indent=2)
        expected = '{\n  "b": 2,\n  "a": 1\n}'
        self.assertEqual(result, expected)
        
        # Unicode characters test (ensure_ascii=False)
        unicode_data = {"name": "John"}
        result = json_dumps(self.mock_ctx, unicode_data, ensure_ascii=False)
        self.assertEqual(result, '{"name": "John"}')
    
    def test_json_loads_basic(self):
        """json_loads filter basic functionality test"""
        # String
        result = json_loads(self.mock_ctx, '"hello"')
        self.assertEqual(result, "hello")
        
        # Number
        result = json_loads(self.mock_ctx, '123')
        self.assertEqual(result, 123)
        
        # Array
        result = json_loads(self.mock_ctx, '[1, 2, 3]')
        self.assertEqual(result, [1, 2, 3])
        
        # Object
        result = json_loads(self.mock_ctx, '{"key": "value"}')
        self.assertEqual(result, {"key": "value"})
    
    def test_json_loads_invalid(self):
        """json_loads filter invalid JSON input test"""
        with self.assertRaises(json.JSONDecodeError):
            json_loads(self.mock_ctx, 'invalid json')
    
    def test_json_escape_strings(self):
        """json_escape filter string test"""
        # Normal string (double quotes removed)
        result = json_escape(self.mock_ctx, "hello world")
        self.assertEqual(result, "hello world")
        
        # String with special characters
        result = json_escape(self.mock_ctx, "hello\nworld")
        self.assertEqual(result, "hello\\nworld")
        
        # String with double quotes
        result = json_escape(self.mock_ctx, 'say "hello"')
        self.assertEqual(result, 'say \\"hello\\"')
        
        # Empty string
        result = json_escape(self.mock_ctx, "")
        self.assertEqual(result, "")
    
    def test_json_escape_non_strings(self):
        """json_escape filter non-string test"""
        # Number（no double quotes so remains as is）
        result = json_escape(self.mock_ctx, 123)
        self.assertEqual(result, '123')
        
        # Array
        result = json_escape(self.mock_ctx, [1, 2, 3])
        self.assertEqual(result, '[1, 2, 3]')
        
        # Object
        result = json_escape(self.mock_ctx, {"key": "value"})
        self.assertEqual(result, '{"key": "value"}')
        
        # null
        result = json_escape(self.mock_ctx, None)
        self.assertEqual(result, 'null')
        
        # boolean
        result = json_escape(self.mock_ctx, True)
        self.assertEqual(result, 'true')
        
        result = json_escape(self.mock_ctx, False)
        self.assertEqual(result, 'false')
    
    def test_json_escape_options(self):
        """json_escape filter options test"""
        data = {"b": 2, "a": 1}
        
        # sort_keys option
        result = json_escape(self.mock_ctx, data, sort_keys=True)
        self.assertEqual(result, '{"a": 1, "b": 2}')
        
        # indent option (object so double quotes are not removed)
        result = json_escape(self.mock_ctx, data, indent=2)
        expected = '{\n  "b": 2,\n  "a": 1\n}'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
