#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004}),
        ("abc", {"login": "abc", "id": 1234567})
    ])
    def test_org(self, org_name, expected_result):
        """
        Test the org method of GithubOrgClient
        
        Args:
            org_name (str): Name of the organization
            expected_result (dict): Expected result from get_json
        """
        # Create GithubOrgClient instance
        org_client = GithubOrgClient(org_name)

        # Use patch to mock get_json and prevent actual HTTP call
        with patch('client.get_json') as mock_get_json:
            # Set the return value for the mocked get_json
            mock_get_json.return_value = expected_result

            # Call the org property (no parentheses!)
            result = org_client.org

            # Assert that the result matches the expected result
            self.assertEqual(result, expected_result)

            # Assert that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )


if __name__ == '__main__':
    unittest.main()
