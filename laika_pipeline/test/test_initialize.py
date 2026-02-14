import unittest
import tempfile

from laika_pipeline import api
from laika_pipeline.db.storage_json import StorageJSON


class TestInitialize(unittest.TestCase):
    """Tests for the initialize() function."""

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_initialize_with_default_parameters(self):
        """Test initialization with default project name and no storage."""
        api.initialize()
        project = api.get_project()
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Default Project")

    def test_initialize_with_custom_name(self):
        """Test initialization with a custom project name."""
        api.initialize(name="Custom Project")
        project = api.get_project()
        self.assertEqual(project.name, "Custom Project")

    def test_initialize_with_storage_backend(self):
        """Test initialization with a custom storage backend."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageJSON(tmpdir)
            api.initialize(name="Stored Project", storage_backend=storage)
            project = api.get_project()
            self.assertEqual(project.name, "Stored Project")
            self.assertIsNotNone(project.storage_backend)

    def test_initialize_overwrites_previous(self):
        """Test that initialize overwrites previous project."""
        api.initialize(name="Project 1")
        project1 = api.get_project()
        api.initialize(name="Project 2")
        project2 = api.get_project()
        self.assertNotEqual(project1.name, project2.name)
        self.assertEqual(project2.name, "Project 2")
