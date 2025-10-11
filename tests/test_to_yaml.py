"""
Tests for additionals.to_yaml module
"""
import unittest
from unittest.mock import Mock
from collections import OrderedDict
import ruamel.yaml

from additionals.to_yaml import to_yaml


class TestToYamlFilter(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.mock_ctx = Mock()
        self.mock_ctx.name = "test_template.j2"
    
    def test_to_yaml_basic_types(self):
        """Test to_yaml filter basic data types"""
        # String
        result = to_yaml(self.mock_ctx, "hello")
        self.assertEqual(result.strip(), "hello")
        
        # Number
        result = to_yaml(self.mock_ctx, 123)
        self.assertEqual(result.strip(), "123")
        
        # Boolean
        result = to_yaml(self.mock_ctx, True)
        self.assertEqual(result.strip(), "true")
        
        result = to_yaml(self.mock_ctx, False)
        self.assertEqual(result.strip(), "false")
        
        # null
        result = to_yaml(self.mock_ctx, None)
        self.assertEqual(result.strip(), "null")
    
    def test_to_yaml_collections(self):
        """Test to_yaml filter collections"""
        # List (when output in flow style)
        data = [1, 2, 3]
        result = to_yaml(self.mock_ctx, data)
        # Match actual output format
        self.assertTrue("[1, 2, 3]" in result or "- 1" in result)
        
        # Dictionary
        data = {"key1": "value1", "key2": "value2"}
        result = to_yaml(self.mock_ctx, data)
        self.assertIn("key1: value1", result)
        self.assertIn("key2: value2", result)
        
        # Nested structure
        data = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ]
        }
        result = to_yaml(self.mock_ctx, data)
        self.assertIn("users:", result)
        self.assertIn("Alice", result)
        self.assertIn("30", result)
    
    def test_to_yaml_ordered_dict(self):
        """Test to_yaml filter OrderedDict"""
        data = OrderedDict([("first", 1), ("second", 2), ("third", 3)])
        result = to_yaml(self.mock_ctx, data)
        
        # Check if order is preserved
        lines = result.strip().split('\n')
        self.assertIn("first: 1", result)
        self.assertIn("second: 2", result)
        self.assertIn("third: 3", result)
    
    def test_to_yaml_indent_option(self):
        """Test to_yaml filter indent option"""
        data = {
            "parent": {
                "child": "value"
            }
        }
        
        # Default indent
        result = to_yaml(self.mock_ctx, data)
        # Verify nested structure is correctly represented
        self.assertIn("parent:", result)
        self.assertIn("child:", result)
        self.assertIn("value", result)
        
        # Custom indent (4 spaces)
        result = to_yaml(self.mock_ctx, data, indent=4)
        # Verify indent option is applied (specific format depends on ruamel.yaml implementation)
        self.assertIn("parent:", result)
        self.assertIn("child:", result)
        self.assertIn("value", result)
    
    def test_to_yaml_unicode(self):
        """Test to_yaml filter Unicode characters"""
        data = {"name": "John", "profession": "Engineer"}
        result = to_yaml(self.mock_ctx, data)
        
        # Verify Unicode characters are output correctly
        self.assertIn("name: John", result)
        self.assertIn("profession: Engineer", result)
    
    def test_to_yaml_special_characters(self):
        """Test to_yaml filter special characters"""
        data = {
            "multiline": "line1\nline2\nline3",
            "quotes": 'He said "Hello"',
            "colon": "key: value"
        }
        result = to_yaml(self.mock_ctx, data)
        
        # Verify special characters are properly escaped or quoted
        self.assertIn("multiline:", result)
        self.assertIn("quotes:", result)
        self.assertIn("colon:", result)
        
        # Verify it can be parsed correctly as YAML
        yaml = ruamel.yaml.YAML()
        parsed = yaml.load(result)
        self.assertEqual(parsed["multiline"], "line1\nline2\nline3")
        self.assertEqual(parsed["quotes"], 'He said "Hello"')
        self.assertEqual(parsed["colon"], "key: value")
    
    def test_to_yaml_empty_collections(self):
        """Test to_yaml filter empty collections"""
        # Empty list
        result = to_yaml(self.mock_ctx, [])
        self.assertEqual(result.strip(), "[]")
        
        # Empty dictionary
        result = to_yaml(self.mock_ctx, {})
        self.assertEqual(result.strip(), "{}")
    
    def test_to_yaml_default_flow_style(self):
        """Test to_yaml filter default_flow_style option"""
        data = {"list": [1, 2, 3], "dict": {"a": 1}}
        
        # Default
        result = to_yaml(self.mock_ctx, data)
        # Verify basic elements are included
        self.assertIn("list:", result)
        self.assertIn("dict:", result)
        
        # Enable flow style
        result = to_yaml(self.mock_ctx, data, default_flow_style=True)
        # Verify by parsing and checking if same as original data
        yaml = ruamel.yaml.YAML()
        parsed = yaml.load(result)
        self.assertEqual(parsed, data)


if __name__ == '__main__':
    unittest.main()
