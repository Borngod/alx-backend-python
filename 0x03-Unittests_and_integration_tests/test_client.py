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
        ({"repos_url": "https://api.github.com/orgs/google/repos"},),
    ])
    @patch('client.get_json')
    def test_public_repos(self, org_payload, mock_get_json):
        """
        Test public_repos method
        
        Args:
            org_payload (dict): Payload for org method
            mock_get_json (Mock): Mocked get_json method
        """
        # Setup mock return values
        mock_get_json.side_effect = [
            org_payload,  # First call for org method
            [  # Second call for repos_payload
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache"}},
                {"name": "repo3"}
            ]
        ]

        # Create GithubOrgClient instance
        org_client = GithubOrgClient("google")

        # Use patch as a context manager to mock _public_repos_url
        with patch.object(org_client, '_public_repos_url', 
                          new_callable=Mock(return_value="https://api.github.com/orgs/google/repos")):
            
            # Call public_repos method
            repos = org_client.public_repos()

            # Verify the list of repos
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            # Check that get_json was called twice (org and repos_payload)
            self.assertEqual(mock_get_json.call_count, 2)

        # Verify that the mocked _public_repos_url property was called
        org_client._public_repos_url

    @parameterized.expand([
        ({"repos_url": "https://api.github.com/orgs/google/repos"},),
    ])
    @patch('client.get_json')
    def test_public_repos_with_license(self, org_payload, mock_get_json):
        """
        Test public_repos method with license filtering
        
        Args:
            org_payload (dict): Payload for org method
            mock_get_json (Mock): Mocked get_json method
        """
        # Setup mock return values
        mock_get_json.side_effect = [
            org_payload,  # First call for org method
            [  # Second call for repos_payload
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache"}},
                {"name": "repo3"}
            ]
        ]

        # Create GithubOrgClient instance
        org_client = GithubOrgClient("google")

        # Use patch as a context manager to mock _public_repos_url
        with patch.object(org_client, '_public_repos_url', 
                          new_callable=Mock(return_value="https://api.github.com/orgs/google/repos")):
            
            # Call public_repos method with license filter
            mit_repos = org_client.public_repos("mit")

            # Verify the list of repos with MIT license
            expected_repos = ["repo1"]
            self.assertEqual(mit_repos, expected_repos)

            # Check that get_json was called twice (org and repos_payload)
            self.assertEqual(mock_get_json.call_count, 2)

        # Verify that the mocked _public_repos_url property was called
        org_client._public_repos_url
        

if __name__ == '__main__':
    unittest.main()
