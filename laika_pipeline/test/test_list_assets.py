import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset


class TestListAssets(unittest.TestCase):
    """Tests for the list_assets() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_list_assets_empty(self):
        """Test listing assets when none exist."""
        assets = api.list_assets()

        self.assertIsInstance(assets, list)
        self.assertEqual(len(assets), 0)

    def test_list_assets_returns_asset_objects(self):
        """Test that list_assets returns Asset objects."""
        asset1 = Asset("hero", "character")
        asset2 = Asset("sword", "prop")

        api.add_asset(asset1)
        api.add_asset(asset2)

        assets = api.list_assets()

        self.assertEqual(len(assets), 2)
        self.assertIsInstance(assets[0], Asset)
        self.assertIsInstance(assets[1], Asset)

    def test_list_assets_correct_order(self):
        """Test that list_assets returns all added assets."""
        asset1 = Asset("alpha", "character")
        asset2 = Asset("beta", "prop")
        asset3 = Asset("gamma", "environment")

        api.add_asset(asset1)
        api.add_asset(asset2)
        api.add_asset(asset3)

        assets = api.list_assets()

        self.assertEqual(len(assets), 3)
        names = [asset.name for asset in assets]
        self.assertIn("alpha", names)
        self.assertIn("beta", names)
        self.assertIn("gamma", names)

    def test_list_assets_after_clear(self):
        """Test that list_assets returns empty after clear."""
        api.add_asset(Asset("test", "character"))
        assets = api.list_assets()
        self.assertEqual(len(assets), 1)

        api.clear()
        api.initialize()
        assets = api.list_assets()
        self.assertEqual(len(assets), 0)
