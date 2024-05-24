#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


""" Integration tests for GithubOrgClient class."""


from typing import List, Dict
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test GithubOrgClient methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])

    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        result = client.org
        expected_url = f"https://api.github.com/orgs/{org_name}"

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"payload": True})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that GithubOrgClient._public_repos_url returns the correct URL.
        """
        expected_repos_url = "https://api.github.com/orgs/test-org/repos"
        mock_org.return_value = {"repos_url": expected_repos_url}

        client = GithubOrgClient("test-org")
        result = client._public_repos_url

        self.assertEqual(result, expected_repos_url)

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the correct list of repos.
        """
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos
        mock_public_repos_url.return_value = "http://fake.url"

        client = GithubOrgClient("test-org")
        result = client.public_repos()

        expected_repos = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected_repos)
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("http://fake.url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])

    def test_has_license(self, repo, license_key, expected):
        """
        Test that GithubOrgClient.has_license returns the correct boolean.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)



@parameterized_class([
    {'org_payload': Dict[str, str]},
    {'repos_payload': List[Dict[str, str]]},
    {'expected_repos': List[str]},
    {'apache2_repos': List[Dict[str, Dict[str, str]]]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls: 'TestIntegrationGithubOrgClient') -> None:
        cls.get_patcher: patch = patch('requests.get')
        cls.mock_get: MagicMock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls: 'TestIntegrationGithubOrgClient') -> None:
        cls.get_patcher.stop()

    def test_public_repos(self: 'TestIntegrationGithubOrgClient') -> None:
        self.mock_get.return_value = MagicMock(json=lambda: self.repos_payload)
        org_client: GithubOrgClient = GithubOrgClient(self.org_payload.get("login"))
        self.assertEqual(org_client.org, self.org_payload.get("login"))
        self.assertEqual(org_client.repos, self.expected_repos)


if __name__ == "__main__":
    unittest.main()
