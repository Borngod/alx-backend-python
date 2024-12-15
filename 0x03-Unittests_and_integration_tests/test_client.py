#!/usr/bin/env python3
"""
Module for unit testing the GithubOrgClient class.

This module contains comprehensive unit tests for the GithubOrgClient class,
including both unit tests and integration tests. It uses parameterized testing
to verify various methods of the GitHub organization client.
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import requests
from fixtures import TEST_PAYLOAD


class MockResponse:
    """
    A mock response class for simulating API responses in testing.

    This class provides a way to mock JSON responses from API calls,
    allowing controlled testing of network-dependent methods.
    """

    def __init__(self, json_data):
        """
        Initialize the MockResponse with JSON data.

        Args:
            json_data (callable): A function that returns JSON data.
        """
        self.json_data = json_data

    def json(self):
        """
        Return the JSON data when called.

        Returns:
            dict: The JSON data from the mocked response.
        """
        return self.json_data()


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.

    This class performs integration tests on the GithubOrgClient,
    verifying its behavior with predefined test payloads.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class-level mocking for HTTP requests.

        This method patches the requests.get method to return predefined
        mock responses for testing purposes.
        """
        cls.get_patcher = patch(
            'requests.get', side_effect=cls.mock_get_response
        )
        cls.get_patcher.start()

    @classmethod
    def mock_get_response(cls, url):
        """
        Mock the response based on the requested URL.

        Args:
            url (str): The URL being requested.

        Returns:
            MockResponse: A mocked response for the given URL.

        Raises:
            ValueError: If an unexpected URL is requested.
        """
        if 'orgs/google' in url:
            if '/repos' in url:
                return MockResponse(lambda: cls.repos_payload)
            return MockResponse(lambda: cls.org_payload)
        raise ValueError("Unexpected URL requested")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the request patcher after tests are complete.

        This method stops the mocking of requests.get to restore
        normal network request behavior.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test retrieving public repositories for an organization.

        Verifies that the public_repos method returns the expected
        list of repository names.
        """
        org_client = GithubOrgClient("google")
        repos = org_client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test retrieving public repositories with a specific license.

        Checks that the public_repos method correctly filters
        repositories by the specified license key.
        """
        org_client = GithubOrgClient("google")
        repos = org_client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test class for GithubOrgClient.

    This class contains unit tests for various methods of the
    GithubOrgClient, ensuring correct functionality of individual
    components.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004}),
        ("abc", {"login": "abc", "id": 1234567})
    ])
    def test_org(self, org_name, expected_result):
        """
        Test the org method of GithubOrgClient.

        Verify that the method returns the correct organization
        information when mocked.

        Args:
            org_name (str): The name of the organization.
            expected_result (dict): The expected organization data.
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

        Ensures that the property returns the correct repositories
        URL for a given organization.
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

        Verifies that the method returns the correct list of
        repository names and makes the expected method calls.

        Args:
            mock_get_json (MagicMock): Mocked get_json function.
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
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test the has_license method of GithubOrgClient.

        Verify that the method correctly determines if a repository
        has a specific license.

        Args:
            repo (dict): Repository information.
            license_key (str): The license key to check.
            expected_result (bool): The expected result of the license check.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
