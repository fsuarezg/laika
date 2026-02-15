"""
Example usage of the LAIKA Asset Validation & Registration Service API.

This demonstrates the clean, module-level API for easy consumption.
"""

import laika_pipeline as lp
from laika_pipeline.db.storage_json import StorageJSON


def example_1_basic_usage():
    """Example 1: Basic load and query operations."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Load and Query")
    print("=" * 70)

    # Initialize with JSON storage
    storage = StorageJSON("sample_data/test_project")
    lp.initialize("VFX Pipeline Project", storage_backend=storage)

    # Load assets from JSON file
    print("\nLoading assets from sample_data/asset_data.json...")
    report = lp.load_assets("sample_data/asset_data.json")
    print(f"  Total processed: {report['total']}")
    print(f"  Valid assets: {report['valid']}")
    if report['errors']:
        print(f"  Errors: {len(report['errors'])}")

    # List all assets
    print("\nListing all assets:")
    assets = lp.list_assets()
    for asset in assets[:5]:  # Show first 5
        print(f"  - {asset.name} ({asset.asset_type.value})")
    if len(assets) > 5:
        print(f"  ... and {len(assets) - 5} more")

    # Get a specific asset
    print("\nGetting specific asset 'hero' of type 'character':")
    hero = lp.get_asset("hero", "character")
    if hero:
        print(f"  Found: {hero}")
        versions = lp.list_asset_versions("hero", "character")
        print(f"  Versions: {len(versions)}")
        for v in versions:
            print(f"    - v{v.version}: {v.department} ({v.status.value})")
    else:
        print("  Asset not found")

    print()


def example_2_add_new_asset():
    """Example 2: Adding new assets programmatically."""
    print("=" * 70)
    print("EXAMPLE 2: Adding New Assets")
    print("=" * 70)

    from laika_pipeline import Asset, AssetVersion

    # Initialize
    lp.initialize("New Project")

    # Create a new asset
    sword = Asset("sword", "prop")

    # Add a version for this asset
    print("\nAdding version for 'sword'...")
    version = AssetVersion(
        asset=sword.code,
        department="modeling",
        version=1,
        status="active"
    )
    version_result = lp.add_asset_version(version)
    print(f"  Added version: {version_result}")

    # Add the new asset
    print("\nAdding a new asset 'sword' of type 'prop'...")
    result = lp.add_asset(sword)
    print(f"  Success: {result['success']}")
    print(f"  Code: {result['asset_code']}")

    # List what we have
    print("\nAll assets created:")
    for asset in lp.list_assets():
        print(f"  - {asset}")

    print()


def example_3_error_handling():
    """Example 3: Error handling during load."""
    print("=" * 70)
    print("EXAMPLE 3: Error Handling")
    print("=" * 70)

    lp.initialize("Error Test Project")

    # Try loading sample data
    print("\nLoading assets with potential errors...")
    report = lp.load_assets("sample_data/asset_data.json")

    print(f"  Total processed: {report['total']}")
    print(f"  Valid: {report['valid']}")
    print(f"  Errors: {len(report['errors'])}")

    if report['errors']:
        print("\nValidation errors encountered:")
        for error in report['errors'][:5]:  # Show first 5
            print(f"  - {error}")
        if len(report['errors']) > 5:
            print(f"  ... and {len(report['errors']) - 5} more")

    # Check internal error log
    print(f"\nTotal validation errors: {len(lp.get_validation_errors())}")

    print()


def main():
    """Run all examples."""
    try:
        example_1_basic_usage()
        example_2_add_new_asset()
        example_3_error_handling()

        print("=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
