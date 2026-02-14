import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset


class TestClear(unittest.TestCase):
    """Tests for the clear() function."""

    def test_clear_resets_state(self):
        """Test that clear resets the API state."""
        api.initialize(name="Test Project")
        api.add_asset(Asset("hero", "character"))

        # Verify project exists
        project = api.get_project()
        self.assertIsNotNone(project)

        # Clear
        api.clear()

        # Verify state is reset
        assert api._project is None

    def test_clear_allows_reinitialization(self):
        """Test that clear allows reinitializing with new settings."""
        api.initialize(name="Project 1")
        api.clear()
        api.initialize(name="Project 2")

        project = api.get_project()
        self.assertEqual(project.name, "Project 2")

    def test_clear_multiple_times(self):
        """Test that clear can be called multiple times."""
        api.initialize()
        api.clear()
        api.clear()

        # Should be able to reinitialize
        api.initialize()
        self.assertIsNotNone(api.get_project())
