import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.project import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


class TestAddAsset(unittest.TestCase):
    """Tests for the add_asset() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_add_asset_success(self):
        """Test successfully adding a valid asset."""
        asset = Asset("hero", "character")
        v1 = AssetVersion(asset.code, "modeling", 1, "active")
        api.add_asset_version(v1)
        result = api.add_asset(asset)

        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['asset_code'])
        self.assertIsNone(result['error'])

    def test_add_asset_returns_asset_code(self):
        """Test that add_asset returns the asset code."""
        asset = Asset("sword", "prop")
        v1 = AssetVersion(asset.code, "modeling", 1, "active")
        api.add_asset_version(v1)
        result = api.add_asset(asset)

        self.assertTrue(result['success'])
        self.assertIsNotNone(result['asset_code'])

    def test_add_asset_multiple_assets(self):
        """Test adding multiple different assets."""
        asset1 = Asset("hero", "character")
        asset2 = Asset("sword", "prop")
        asset3 = Asset("forest", "environment")

        # Add versions to each asset
        v1 = AssetVersion(asset1.code, "modeling", 1, "active")
        v2 = AssetVersion(asset2.code, "modeling", 1, "active")
        v3 = AssetVersion(asset3.code, "modeling", 1, "active")
        api.add_asset_version(v1)
        api.add_asset_version(v2)
        api.add_asset_version(v3)

        result1 = api.add_asset(asset1)
        result2 = api.add_asset(asset2)
        result3 = api.add_asset(asset3)
        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])
        self.assertTrue(result3['success'])

        assets = api.list_assets()
        self.assertEqual(len(assets), 3)

    def test_add_duplicate_asset_fails(self):
        """Test that adding duplicate asset fails."""
        asset1 = Asset("hero", "character")
        asset2 = Asset("hero", "character")

        v1 = AssetVersion(asset1.code, "modeling", 1, "active")
        api.add_asset_version(v1)

        result1 = api.add_asset(asset1)
        result2 = api.add_asset(asset2)

        self.assertTrue(result1['success'])
        self.assertFalse(result2['success'])
        self.assertIsNotNone(result2['error'])

    def test_add_asset_returns_result_dict_structure(self):
        """Test that result dict has correct structure."""
        asset = Asset("test", "character")
        result = api.add_asset(asset)

        self.assertIn('success', result)
        self.assertIn('asset_code', result)
        self.assertIn('error', result)
