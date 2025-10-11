"""
Tests for additionals.color module
"""
import unittest
from unittest.mock import Mock, patch
import os
from colour import Color

from additionals.color import (
    is_success, is_failure, status_success_color, status_failure_color,
    status_other_color, actions_status_color, outcome_color, status_color,
    discord_color
)


class TestColorFilters(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.mock_ctx = Mock()
        self.mock_ctx.name = "test_template.j2"
    
    def test_is_success_string_values(self):
        """is_success filter string values test"""
        # Success strings
        success_values = ["success", "succeeded", "pass", "passed", "ok"]
        for value in success_values:
            with self.subTest(value=value):
                result = is_success(self.mock_ctx, value)
                self.assertTrue(result)
                
                # Verify it works with uppercase
                result = is_success(self.mock_ctx, value.upper())
                self.assertTrue(result)
        
        # Failure strings
        failure_values = ["failure", "failed", "fail", "error", "errored", "ng"]
        for value in failure_values:
            with self.subTest(value=value):
                result = is_success(self.mock_ctx, value)
                self.assertFalse(result)
        
        # Other strings
        other_values = ["unknown", "pending", "running"]
        for value in other_values:
            with self.subTest(value=value):
                result = is_success(self.mock_ctx, value)
                self.assertFalse(result)
    
    def test_is_success_non_string_values(self):
        """is_success filter non-string values test"""
        # Truthy values
        truthy_values = [1, -1, [1], {"key": "value"}, True]
        for value in truthy_values:
            with self.subTest(value=value):
                result = is_success(self.mock_ctx, value)
                self.assertTrue(result)
        
        # Falsy values
        falsy_values = [0, [], {}, None, False, ""]
        for value in falsy_values:
            with self.subTest(value=value):
                result = is_success(self.mock_ctx, value)
                self.assertFalse(result)
    
    def test_is_failure_string_values(self):
        """is_failure filter string values test"""
        # Failure strings
        failure_values = ["failure", "failed", "fail", "error", "errored", "ng"]
        for value in failure_values:
            with self.subTest(value=value):
                result = is_failure(self.mock_ctx, value)
                self.assertTrue(result)
                
                # Verify it works with uppercase
                result = is_failure(self.mock_ctx, value.upper())
                self.assertTrue(result)
        
        # Success strings
        success_values = ["success", "succeeded", "pass", "passed", "ok"]
        for value in success_values:
            with self.subTest(value=value):
                result = is_failure(self.mock_ctx, value)
                self.assertFalse(result)
        
        # Other strings
        other_values = ["unknown", "pending", "running"]
        for value in other_values:
            with self.subTest(value=value):
                result = is_failure(self.mock_ctx, value)
                self.assertFalse(result)
    
    def test_is_failure_non_string_values(self):
        """is_failure filter non-string values test"""
        # Truthy values
        truthy_values = [1, -1, [1], {"key": "value"}, True]
        for value in truthy_values:
            with self.subTest(value=value):
                result = is_failure(self.mock_ctx, value)
                self.assertTrue(result)
        
        # Falsy values
        falsy_values = [0, [], {}, None, False, ""]
        for value in falsy_values:
            with self.subTest(value=value):
                result = is_failure(self.mock_ctx, value)
                self.assertFalse(result)
    
    def test_status_success_color_default(self):
        """status_success_color default value test"""
        with patch.dict(os.environ, {}, clear=True):
            result = status_success_color()
            expected = Color('#1f883d')
            self.assertEqual(result.hex_l, expected.hex_l)
    
    @patch.dict(os.environ, {'KAMIDANA_STATUS_SUCCESS': '#00ff00'})
    def test_status_success_color_custom(self):
        """status_success_color custom value test"""
        result = status_success_color()
        expected = Color('#00ff00')
        self.assertEqual(result.hex_l, expected.hex_l)
    
    def test_status_failure_color_default(self):
        """status_failure_color default value test"""
        with patch.dict(os.environ, {}, clear=True):
            result = status_failure_color()
            expected = Color('#cf222e')
            self.assertEqual(result.hex_l, expected.hex_l)
    
    @patch.dict(os.environ, {'KAMIDANA_STATUS_FAILURE': '#ff0000'})
    def test_status_failure_color_custom(self):
        """status_failure_color custom value test"""
        result = status_failure_color()
        expected = Color('#ff0000')
        self.assertEqual(result.hex_l, expected.hex_l)
    
    def test_status_other_color_default(self):
        """status_other_color default value test"""
        with patch.dict(os.environ, {}, clear=True):
            result = status_other_color()
            expected = Color('#6e7781')
            self.assertEqual(result.hex_l, expected.hex_l)
    
    @patch.dict(os.environ, {'KAMIDANA_STATUS_OTHER': '#888888'})
    def test_status_other_color_custom(self):
        """status_other_color custom value test"""
        result = status_other_color()
        expected = Color('#888888')
        self.assertEqual(result.hex_l, expected.hex_l)
    
    def test_actions_status_color(self):
        """actions_status_color filter test"""
        # Success status
        result = actions_status_color(self.mock_ctx, 'success')
        expected = status_success_color()
        self.assertEqual(result.hex_l, expected.hex_l)
        
        result = actions_status_color(self.mock_ctx, 'SUCCESS')
        self.assertEqual(result.hex_l, expected.hex_l)
        
        # Failure status
        result = actions_status_color(self.mock_ctx, 'failure')
        expected = status_failure_color()
        self.assertEqual(result.hex_l, expected.hex_l)
        
        result = actions_status_color(self.mock_ctx, 'FAILURE')
        self.assertEqual(result.hex_l, expected.hex_l)
        
        # Other statuses
        other_statuses = ['pending', 'running', 'cancelled', 'unknown']
        expected = status_other_color()
        for status in other_statuses:
            with self.subTest(status=status):
                result = actions_status_color(self.mock_ctx, status)
                self.assertEqual(result.hex_l, expected.hex_l)
    
    def test_outcome_color(self):
        """outcome_color filter test（actions_status_color alias）"""
        # Success status
        result = outcome_color(self.mock_ctx, 'success')
        expected = status_success_color()
        self.assertEqual(result.hex_l, expected.hex_l)
        
        # Failure status
        result = outcome_color(self.mock_ctx, 'failure')
        expected = status_failure_color()
        self.assertEqual(result.hex_l, expected.hex_l)
    
    def test_status_color(self):
        """status_color filter test"""
        # Values representing success
        success_values = ["success", "ok", "passed"]
        expected_success = status_success_color()
        for value in success_values:
            with self.subTest(value=value):
                result = status_color(self.mock_ctx, value)
                self.assertEqual(result.hex_l, expected_success.hex_l)
        
        # Values representing failure
        failure_values = ["failure", "error", "failed"]
        expected_failure = status_failure_color()
        for value in failure_values:
            with self.subTest(value=value):
                result = status_color(self.mock_ctx, value)
                self.assertEqual(result.hex_l, expected_failure.hex_l)
        
        # Other values
        other_values = ["pending", "unknown", "running"]
        expected_other = status_other_color()
        for value in other_values:
            with self.subTest(value=value):
                result = status_color(self.mock_ctx, value)
                self.assertEqual(result.hex_l, expected_other.hex_l)
    
    def test_discord_color(self):
        """discord_color filter test"""
        # Red
        result = discord_color(self.mock_ctx, "#ff0000")
        self.assertEqual(result, 16711680)  # 0xff0000
        
        # Green
        result = discord_color(self.mock_ctx, "#00ff00")
        self.assertEqual(result, 65280)  # 0x00ff00
        
        # Blue
        result = discord_color(self.mock_ctx, "#0000ff")
        self.assertEqual(result, 255)  # 0x0000ff
        
        # White
        result = discord_color(self.mock_ctx, "#ffffff")
        self.assertEqual(result, 16777215)  # 0xffffff
        
        # Black
        result = discord_color(self.mock_ctx, "#000000")
        self.assertEqual(result, 0)  # 0x000000
        
        # Custom color
        result = discord_color(self.mock_ctx, "#1f883d")
        expected = int("1f883d", 16)
        self.assertEqual(result, expected)
        
        # Also test with Color object input
        color_obj = Color("#ff0000")
        result = discord_color(self.mock_ctx, color_obj)
        self.assertEqual(result, 16711680)


if __name__ == '__main__':
    unittest.main()
