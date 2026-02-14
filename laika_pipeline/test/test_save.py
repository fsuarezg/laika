import unittest
import tempfile

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.db.storage_json import StorageJSON


class TestSave(unittest.TestCase):
    """Tests for the save() function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageJSON(self.temp_dir.name)
        api.initialize(name="SaveTest", storage_backend=self.storage)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()
        self.temp_dir.cleanup()

    def test_save_returns_result_dict(self):
        """Test that save() returns proper result dict."""
        result = api.save()

        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('error', result)

    def test_save_with_assets(self):
        """Test saving with assets in project."""
        asset = Asset("hero", "character")
        api.add_asset(asset)

        result = api.save()

        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])

    def test_save_empty_project(self):
        """Test saving empty project."""
        result = api.save()

        self.assertTrue(result['success'])

    def test_save_multiple_times(self):
        """Test saving multiple times."""
        result1 = api.save()
        result2 = api.save()

        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])

    def test_save_without_storage(self):
        """Test save without storage backend (in-memory)."""
        api.clear()
        api.initialize()

        result = api.save()

        # In-memory storage may handle this differently
        self.assertIsInstance(result, dict)
