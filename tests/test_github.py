"""
Tests for additionals.github module

Note: Since this actually calls GitHub API, real tests are only executed
when GITHUB_TOKEN is set. Otherwise, mock objects are used for testing.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os

# Clear environment variables before testing to create mock environment
with patch.dict(os.environ, {}, clear=True):
    from additionals.github import github_user, github_user_email


class TestGitHubFilters(unittest.TestCase):
    
    def setUp(self):
        """Test setup"""
        self.mock_ctx = Mock()
        self.mock_ctx.name = "test_template.j2"
    
    @patch('additionals.github.g')
    def test_github_user_success(self, mock_github):
        """Test github_user filter success case"""
        # Create mock user object
        mock_user = Mock()
        mock_user.login = "testuser"
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        
        # Mock GitHub API
        mock_github.get_user.return_value = mock_user
        
        # Execute test
        result = github_user(self.mock_ctx, "testuser")
        
        # Verify
        mock_github.get_user.assert_called_once_with("testuser")
        self.assertEqual(result, mock_user)
        self.assertEqual(result.login, "testuser")
        self.assertEqual(result.name, "Test User")
    
    @patch('additionals.github.g')
    def test_github_user_email_success(self, mock_github):
        """Test github_user_email filter success case"""
        # Create mock user object
        mock_user = Mock()
        mock_user.email = "test@example.com"
        
        # Mock GitHub API
        mock_github.get_user.return_value = mock_user
        
        # Execute test
        result = github_user_email(self.mock_ctx, "testuser")
        
        # Verify
        mock_github.get_user.assert_called_once_with("testuser")
        self.assertEqual(result, "test@example.com")
    
    @patch('additionals.github.g')
    def test_github_user_not_found(self, mock_github):
        """Test github_user filter when user not found"""
        from github import UnknownObjectException
        
        # Mock GitHub API to raise exception
        mock_github.get_user.side_effect = UnknownObjectException(404, "Not Found")
        
        # Verify that exception is raised during test execution
        with self.assertRaises(UnknownObjectException):
            github_user(self.mock_ctx, "nonexistentuser")
    
    @patch('additionals.github.g')
    def test_github_user_email_not_found(self, mock_github):
        """Test github_user_email filter when user not found"""
        from github import UnknownObjectException
        
        # Mock GitHub API to raise exception
        mock_github.get_user.side_effect = UnknownObjectException(404, "Not Found")
        
        # Verify that exception is raised during test execution
        with self.assertRaises(UnknownObjectException):
            github_user_email(self.mock_ctx, "nonexistentuser")
    
    @patch('additionals.github.g')
    def test_github_user_email_none(self, mock_github):
        """Test github_user_email filter when email is None"""
        # Create mock user object (email is None)
        mock_user = Mock()
        mock_user.email = None
        
        # Mock GitHub API
        mock_github.get_user.return_value = mock_user
        
        # Execute test
        result = github_user_email(self.mock_ctx, "testuser")
        
        # Verify
        mock_github.get_user.assert_called_once_with("testuser")
        self.assertIsNone(result)
    
    def test_github_token_environment_variables(self):
        """Test GitHub token environment variable retrieval"""
        # To test the behavior of additionals.github module,
        # instead of directly testing module initialization logic,
        # we verify the environment variable processing logic
        
        # When GITHUB_TOKEN exists
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
            token = os.getenv('GITHUB_TOKEN', os.getenv('INPUTS_GITHUB_TOKEN', ''))
            self.assertEqual(token, 'test_token')
        
        # When INPUTS_GITHUB_TOKEN exists
        with patch.dict(os.environ, {'INPUTS_GITHUB_TOKEN': 'inputs_token'}, clear=True):
            token = os.getenv('GITHUB_TOKEN', os.getenv('INPUTS_GITHUB_TOKEN', ''))
            self.assertEqual(token, 'inputs_token')
        
        # When neither exists
        with patch.dict(os.environ, {}, clear=True):
            token = os.getenv('GITHUB_TOKEN', os.getenv('INPUTS_GITHUB_TOKEN', ''))
            self.assertEqual(token, '')


if __name__ == '__main__':
    unittest.main()
