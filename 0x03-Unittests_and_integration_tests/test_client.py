#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org method returns correct value."""
        # Setup mock behavior
        mock_get_json.return_value = {"test_key": "test_value"}

        # Instantiate the client
        client = GithubOrgClient(org_name)

        # Call the method being tested
        result = client.org()

        # Assertions
        self.assertEqual(result, {"test_key": "test_value"})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == '__main__':
    unittest.main()
