import unittest
import tempfile

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.db.storage_json import StorageJSON


class TestLoad(unittest.TestCase):
    """Tests for the load() function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageJSON(self.temp_dir.name)
        api.initialize(name="LoadTest", storage_backend=self.storage)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()
        self.temp_dir.cleanup()

    def test_load_returns_result_dict(self):
        """Test that load() returns proper result dict."""
        result = api.load()

        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('error', result)

    def test_load_empty_storage(self):
        """Test loading from empty storage."""
        result = api.load()

        self.assertTrue(result['success'])

    def test_load_after_save(self):
        """Test load after saving assets."""
        # Add and save assets
        asset = Asset("hero", "character")
        api.add_asset(asset)
        save_result = api.save()
        self.assertTrue(save_result['success'])

        # Clear and reload
        api.clear()
        api.initialize(name="LoadTest2", storage_backend=self.storage)

        load_result = api.load()
        self.assertTrue(load_result['success'])

    def test_load_preserves_data(self):
        """Test that load preserves saved data."""
        # Save some assets
        asset1 = Asset("hero", "character")
        asset2 = Asset("sword", "prop")
        api.add_asset(asset1)
        api.add_asset(asset2)
        api.save()

        # Clear and reload
        saved_count = len(api.list_assets())
        api.clear()
        api.initialize(name="LoadTest3", storage_backend=self.storage)
        api.load()

        loaded_count = len(api.list_assets())
        self.assertEqual(saved_count, loaded_count)
