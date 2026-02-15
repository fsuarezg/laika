import unittest
import tempfile

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.db.storage_json import StorageJSON


class TestAPIScenarios(unittest.TestCase):
    """API tests for complete workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageJSON(self.temp_dir.name)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()
        self.temp_dir.cleanup()

    def test_full_workflow_create_save_load(self):
        """Test complete workflow: create, save, and load."""
        # Create
        api.initialize("Workflow Test", self.storage)
        asset = Asset("hero", "character")
        api.add_asset(asset)

        # Save
        save_result = api.save()
        self.assertTrue(save_result['success'])

        # Clear and load
        assets_count = len(api.list_assets())
        api.clear()
        api.initialize("Workflow Test 2", self.storage)
        load_result = api.load()
        self.assertTrue(load_result['success'])

        # Verify
        loaded_assets = api.list_assets()
        self.assertEqual(len(loaded_assets), assets_count)

    def test_workflow_add_multiple_assets_with_versions(self):
        """Test workflow with multiple assets and versions."""
        api.initialize()

        # Add assets
        asset1 = Asset("hero", "character")
        asset2 = Asset("villain", "character")
        
        # Add versions
        v1 = AssetVersion(asset1.code, "modeling", 1, "active")
        v2 = AssetVersion(asset1.code, "texturing", 1, "active")
        v3 = AssetVersion(asset2.code, "modeling", 1, "inactive")

        api.add_asset_version(v1)
        api.add_asset_version(v2)
        api.add_asset_version(v3)
        api.add_asset(asset1)
        api.add_asset(asset2)

        # Verify
        self.assertEqual(len(api.list_assets()),
                         2)
        self.assertEqual(len(api.list_asset_versions("hero", "character")),
                         2)
        self.assertEqual(len(api.list_asset_versions("villain", "character")),
                         1)

    def test_workflow_duplicate_prevention(self):
        """Test that duplicates are properly rejected."""
        api.initialize()

        asset1 = Asset("hero", "character")
        asset2 = Asset("hero", "character")

        v1 = AssetVersion(asset1.code, "modeling", 1)
        api.add_asset_version(v1)

        result1 = api.add_asset(asset1)
        result2 = api.add_asset(asset2)

        self.assertTrue(result1['success'])
        self.assertFalse(result2['success'])
        self.assertEqual(len(api.list_assets()), 1)

    def test_workflow_asset_retrieval(self):
        """Test retrieving assets after operations."""
        api.initialize()

        # Add multiple assets
        assets_to_add = [
            Asset("hero", "character"),
            Asset("villain", "character"),
            Asset("sword", "prop"),
            Asset("castle", "environment")
        ]

        # Add versions for each asset
        for asset in assets_to_add:
            version = AssetVersion(asset.code, "modeling", 1, "active")
            api.add_asset_version(version)

        for asset in assets_to_add:
            api.add_asset(asset)

        # Retrieve specific assets
        hero = api.get_asset("hero", "character")
        sword = api.get_asset("sword", "prop")

        self.assertIsNotNone(hero)
        self.assertIsNotNone(sword)
        self.assertEqual(hero.name, "hero")
        self.assertEqual(sword.name, "sword")
