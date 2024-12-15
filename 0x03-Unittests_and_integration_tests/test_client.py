#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
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
        """
        org_client = GithubOrgClient(org_name)

        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = expected_result
            result = org_client.org
            self.assertEqual(result, expected_result)
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )
    def test_public_repos_url(self):
        """
        Test the _public_repos_url property of GithubOrgClient
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        org_client = GithubOrgClient("google")

        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.side_effect = lambda: mock_payload  # Use side_effect for property
            result = org_client._public_repos_url
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
            mock_repos_url.side_effect = lambda: "https://api.github.com/orgs/google/repos"

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
