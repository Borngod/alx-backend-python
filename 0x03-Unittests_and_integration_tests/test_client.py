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
            mock_org.return_value = mock_payload
            result = org_client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient
        """
        # Mock payload for public repositories
        mock_payload = {
            "repos": ["repo1", "repo2", "repo3"]
        }
        
        # Mock the _public_repos_url property
        mock_repos_url = "mocked_repos_url"

        # Setup the mocks
        mock_get_json.return_value = mock_payload
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_property:
            mock_property.return_value = mock_repos_url

            # Create an instance of GithubOrgClient
            org_client = GithubOrgClient("google")

            # Call the method under test
            result = org_client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(mock_repos_url)
            mock_property.assert_called_once()


if __name__ == '__main__':
    unittest.main()
