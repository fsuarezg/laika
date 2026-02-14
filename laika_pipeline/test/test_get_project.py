import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset


class TestGetProject(unittest.TestCase):
    """Tests for the get_project() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_get_project_returns_project(self):
        """Test that get_project returns a Project instance."""
        from laika_pipeline.pipeline.project import Project

        project = api.get_project()

        self.assertIsInstance(project, Project)

    def test_get_project_consistent(self):
        """Test that get_project returns same instance."""
        project1 = api.get_project()
        project2 = api.get_project()

        self.assertIs(project1, project2)

    def test_get_project_has_expected_attributes(self):
        """Test that project has expected attributes."""
        project = api.get_project()

        self.assertTrue(hasattr(project, 'name'))
        self.assertTrue(hasattr(project, 'assets'))
        self.assertTrue(hasattr(project, 'asset_versions'))

    def test_get_project_after_operations(self):
        """Test get_project after various operations."""
        api.add_asset(Asset("hero", "character"))
        project = api.get_project()

        self.assertEqual(len(project.assets), 1)

    def test_get_project_initializes_if_needed(self):
        """Test that get_project initializes if not yet initialized."""
        api.clear()

        project = api.get_project()

        self.assertIsNotNone(project)
