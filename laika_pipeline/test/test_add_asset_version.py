import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


class TestAddAssetVersion(unittest.TestCase):
    """Tests for the add_asset_version() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()
        # Add a base asset first
        self.asset = Asset("hero", "character")
        api.add_asset(self.asset)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_add_asset_version_success(self):
        """Test successfully adding a valid asset version."""
        version = AssetVersion(
            asset=self.asset.code,
            department="modeling",
            version=1,
            status="active"
        )
        result = api.add_asset_version(version)

        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['asset_code'])
        self.assertIsNotNone(result['version'])

    def test_add_asset_version_incremental(self):
        """Test adding multiple versions of the same asset."""
        v1 = AssetVersion(self.asset.code, "modeling", 1, "active")
        v2 = AssetVersion(self.asset.code, "texturing", 1, "active")

        result1 = api.add_asset_version(v1)
        result2 = api.add_asset_version(v2)

        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])

    def test_add_asset_version_duplicate_fails(self):
        """Test that duplicate versions are rejected."""
        v1 = AssetVersion(self.asset.code, "modeling", 1, "active")
        v2 = AssetVersion(self.asset.code, "modeling", 1, "active")

        result1 = api.add_asset_version(v1)
        result2 = api.add_asset_version(v2)

        self.assertTrue(result1['success'])
        self.assertFalse(result2['success'])

    def test_add_asset_version_returns_result_dict_structure(self):
        """Test that result dict has correct structure."""
        version = AssetVersion(self.asset.code, "modeling", 1, "active")
        result = api.add_asset_version(version)

        self.assertIn('success', result)
        self.assertIn('asset_code', result)
        self.assertIn('version', result)
        self.assertIn('error', result)
