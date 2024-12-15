#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import requests
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos, "apache2_repos": apache2_repos}
    for org_payload, repos_payload, expected_repos, apache2_repos in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    def __init_subclass__(cls, **kwargs):
        cls.org_payload = kwargs.get('org_payload')
        cls.repos_payload = kwargs.get('repos_payload')
        cls.expected_repos = kwargs.get('expected_repos')
        cls.apache2_repos = kwargs.get('apache2_repos')

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get', side_effect=cls.mock_get_response)
        cls.get_patcher.start()

    @classmethod
    def mock_get_response(cls, url):
        """Mock the response based on URL."""
        if 'orgs/google' in url:
            if '/repos' in url:
                return MockResponse(lambda: cls.repos_payload)
            else:
                return MockResponse(lambda: cls.org_payload)
        raise ValueError("Unexpected URL requested")

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        org_client = GithubOrgClient("google")
        repos = org_client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        org_client = GithubOrgClient("google")
        repos = org_client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004}),
        ("abc", {"login": "abc", "id": 1234567})
    ])
    def test_org(self, org_name, expected_result):
        """
        Test the org method of GithubOrgClient.
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
        Test the _public_repos_url property of GithubOrgClient.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        org_client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload
            result = org_client._public_repos_url
            self.assertEqual(
                result, "https://api.github.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient.
        """
        # Mock payload for public repositories
        mock_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"}
        ]

        # Mock the _public_repos_url property
        mock_repos_url = "mocked_repos_url"

        # Setup the mocks
        mock_get_json.return_value = mock_payload
        with patch.object(
            GithubOrgClient, '_public_repos_url', new_callable=PropertyMock
        ) as mock_property:
            mock_property.return_value = mock_repos_url

            # Create an instance of GithubOrgClient
            org_client = GithubOrgClient("google")

            # Call the method under test without specifying a license
            result = org_client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(mock_repos_url)
            mock_property.assert_called_once()
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test the has_license method of GithubOrgClient.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
