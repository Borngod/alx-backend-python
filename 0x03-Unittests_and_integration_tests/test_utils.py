#!/usr/bin/env python3
"""
Unit tests for the nested map access utility module.

This module contains comprehensive unit tests to verify the 
functionality of the access_nested_map function from the utils module.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.

    Provides parameterized tests to verify correct navigation
    and value retrieval from nested dictionary structures.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Parameterized test method to check access_nested_map function.

        Args:
            nested_map (dict): Input nested dictionary
            path (tuple): Path to access in the nested dictionary
            expected: Expected return value
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, key):
        """
        Parameterized test method to check KeyError raising in access_nested_map.

        Args:
            nested_map (dict): Input nested dictionary
            path (tuple): Path to access in the nested dictionary
            key (str): The key expected to cause the KeyError
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        self.assertEqual(str(context.exception), repr(key))


from unittest.mock import patch, Mock
from utils import get_json


class TestGetJson(unittest.TestCase):
    """
    Test case for the get_json function.

    Provides tests to verify correct behavior of JSON retrieval 
    from URLs using mocked HTTP requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Parameterized test method to check get_json function.

        Args:
            test_url (str): URL to retrieve JSON from
            test_payload (dict): Expected JSON payload
        """
        # Create a mock response with a json method
        with patch('requests.get') as mock_get:
            # Configure the mock to return a mock with the specified json payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function and verify results
            result = get_json(test_url)

            # Verify the mock was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Verify the returned result matches the test payload
            self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
