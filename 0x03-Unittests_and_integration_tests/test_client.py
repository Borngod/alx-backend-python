#!/usr/bin/env python3
"""
Unit tests for the GitHub Organization Client.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name):
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): Name of the GitHub organization to test
        """
        # Create test configuration
        test_payload = {"name": org_name}
        
        # Use patch to mock get_json and prevent external HTTP calls
        with patch('client.get_json') as mock_get_json:
            # Set the return value for the mocked get_json
            mock_get_json.return_value = test_payload
            
            # Create GithubOrgClient instance
            gh_client = GithubOrgClient(org_name)
            
            # Call the org method
            result = gh_client.org()
            
            # Verify get_json was called with correct URL
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )
            
            # Verify the returned result matches the test payload
            self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
