import unittest

from laika_pipeline import api


class TestGetValidationErrors(unittest.TestCase):
    """Tests for the get_validation_errors() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_get_validation_errors_empty(self):
        """Test getting validation errors when none exist."""
        errors = api.get_validation_errors()

        self.assertIsInstance(errors, list)

    def test_get_validation_errors_returns_list(self):
        """Test that get_validation_errors returns a list."""
        errors = api.get_validation_errors()

        self.assertIsInstance(errors, list)

    def test_get_validation_errors_contains_strings(self):
        """Test that validation errors are strings."""
        errors = api.get_validation_errors()

        for error in errors:
            self.assertIsInstance(error, str)
