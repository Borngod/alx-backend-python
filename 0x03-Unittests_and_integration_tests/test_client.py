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
    def test_public_repos_url(self):
        """
        Test the _public_repos_url property of GithubOrgClient
        """
        # Mock payload for org
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        # Create an instance of GithubOrgClient
        org_client = GithubOrgClient("google")

        # Use patch as context manager to mock the `org` property
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            # Set the return value of the mocked org property
            mock_org.return_value = mock_payload

            # Access the _public_repos_url property
            result = org_client._public_repos_url

            # Assert that the result matches the expected repos_url
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient
        """
        # Mock payload for get_json
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        # Mock the get_json function to return the payload
        mock_get_json.return_value = mock_repos_payload

        # Create an instance of GithubOrgClient
        org_client = GithubOrgClient("google")

        # Use patch as context manager to mock _public_repos_url
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=property) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"

            # Call public_repos and get the result
            result = org_client.public_repos()

            # Assert the result matches the names in the mocked payload
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Assert the mocked property was called once
            mock_repos_url.assert_called_once()

            # Assert get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

if __name__ == '__main__':
    unittest.main()
