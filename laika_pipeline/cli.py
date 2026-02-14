
import sys
import argparse
import signal
import os
import json

import laika_pipeline as lp
from laika_pipeline.lib.load_json import load_json
from laika_pipeline.db.storage_json import StorageJSON


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project_name', '-p',
        default='Default Project',
        help='Project name'
    )
    parser.add_argument(
        '--json_path', '-jp',
        help='Path to the project json file repository, can be either a'
        ' directory (for JSON storage) or a single JSON file from which to'
        'load assets and versions'
    )
    return parser.parse_args()


def cmd_load(args):
    """Load assets from a JSON file."""
    if not args:
        print("Error: load requires a file path")
        return
    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    try:
        report = lp.load_assets(filepath)
        print(f"Loaded {report['valid']} valid assets")
        if report['errors']:
            print(f"{len(report['errors'])} errors during load:")
            for err in report['errors'][:5]:
                print(f"  - {err}")
            if len(report['errors']) > 5:
                print(f"  ... and {len(report['errors']) - 5} more")
    except Exception as e:
        print(f"Error loading assets: {e}")


def cmd_add(args):
    """Add a new asset from a JSON file."""
    if not args:
        print("Error: add requires a file path")
        return
    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    try:
        data = load_json(filepath)
        asset = lp.Asset(data['name'], data['asset_type'])
        result = lp.add_asset(asset)
        if result['success']:
            print(f"Asset added: {asset.name} ({asset.asset_type.value})")
            print(f"Code: {result['asset_code']}")
        else:
            print(f"Failed to add asset: {result['error']}")
    except Exception as e:
        print(f"Error adding asset: {e}")


def cmd_get(args):
    """Get a specific asset by name and type."""
    if len(args) < 2:
        print("Error: get requires <asset_name> <asset_type>")
        return
    name, asset_type = args[0], args[1]
    asset = lp.get_asset(name, asset_type)
    if asset:
        print("Found asset:")
        print(f"Name: {asset.name}")
        print(f"Asset Type: {asset.asset_type.value}")
        print(f"Code: {asset.code}")
    else:
        print(f"Asset not found: {name} ({asset_type})")


def cmd_list(args):
    """List all assets."""
    assets = lp.list_assets()
    if not assets:
        print("No assets loaded.")
        return
    print(f"{len(assets)} assets:")
    for asset in assets:
        print(f"  - {asset.name} ({asset.asset_type.value})"
              f" [code: {asset.code}]")


def cmd_versions_add(args):
    """Add a new asset version from a JSON file."""
    # NOTE: I struggled with implementing the add versions command as specified
    # in the task description, which was to have the user run
    # `versions add <asset_name> <version.json>`.
    # The main issue is that asset_name is not unique across the project -
    # you need both the asset_name and asset_type to identify the asset to
    # which the version belongs.
    print(args)
    if len(args) < 3:
        print("Error: versions add requires "
              "<asset_name> <asset_type> <version.json>")
        return
    asset_name, asset_type, filepath = args[0], args[1], args[2]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    try:
        data = load_json(filepath)

        asset = lp.get_asset(asset_name, asset_type)
        if not asset:
            print(f"Error: Asset not found: {asset_name} ({asset_type})")
            return

        version = lp.AssetVersion(
            asset=asset.code,
            department=data['department'],
            version=data['version'],
            status=data.get('status', 'active')
        )
        result = lp.add_asset_version(version)
        if result['success']:
            print("Version added:")
            print(f"Asset: {asset_name}")
            print(f"Department: {data['department']}")
            print(f"Version: {data['version']}")
        else:
            print(f"Failed to add version: {result['error']}")
    except Exception as e:
        print(f"Error adding version: {e}")


def cmd_versions_get(args):
    """Get a specific asset version."""
    if len(args) < 3:
        print("Error: versions get requires "
              "<asset_name> <asset_type> <version_num>")
        return
    asset_name, asset_type, version_num = args[0], args[1], args[2]
    try:
        version_num = int(version_num)
    except ValueError:
        print("Error: version_num must be an integer")
        return

    version = lp.get_asset_version(asset_name, asset_type, version_num)
    if version:
        print("Found version:")
        print(f"Asset: {asset_name} ({asset_type})")
        print(f"Department: {version.department}")
        print(f"Version: {version.version}")
        print(f"Status: {version.status.value}")
    else:
        print(f"Version not found: {asset_name} ({asset_type}) v{version_num}")


def cmd_versions_list(args):
    """List all versions of an asset."""
    if len(args) < 2:
        print("Error: versions list requires <asset_name> <asset_type>")
        return
    asset_name, asset_type = args[0], args[1]
    versions = lp.list_asset_versions(asset_name, asset_type)
    if not versions:
        print(f"No versions found for {asset_name} ({asset_type})")
        return
    print(f"{len(versions)} versions of {asset_name} ({asset_type}):")
    for v in sorted(versions, key=lambda x: x.version):
        print(f"  v{v.version} - {v.department} - {v.status.value}")


def cmd_save(args):
    """Save the project to storage."""
    result = lp.save()
    if result['success']:
        print("Project saved successfully")
    else:
        print(f"Failed to save project: {result['error']}")


def cmd_load_project(args):
    """Load the project from storage.
    This will load assets from the storage backend"""
    result = lp.load()
    if result['success']:
        print("Project loaded successfully")
    else:
        print(f"Failed to load project: {result['error']}")


def cmd_errors(args):
    """Show validation errors."""
    errors = lp.get_validation_errors()
    if not errors:
        print("No validation errors")
        return
    print(f"{len(errors)} validation errors:")
    for err in errors[:10]:
        print(f"  - {err}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")


def cmd_help(args):
    help_text = """
    Available commands:
    load <file.json>                           Load assets from JSON file
    add <asset.json>                           Add a new asset from JSON file
    get <asset_name> <type>                    Get an asset by name and type
    list                                       List all assets
    versions add <asset_name> <asset_type> <version.json>   Add a version for an asset
    versions get <asset_name> <asset_type> <version> Get a specific asset version
    versions list <asset_name> <asset_type>          List all versions of an asset
    save                                       Save project to storage
    load_project                               Load project from storage
    errors                                     Show validation errors
    help                                       Show this help message
    exit                                       Exit the CLI
    """
    print(help_text)


def _print_welcome():
    print("Welcome to the Laika Pipeline CLI!")
    logo = """
                                #####
                          ##  ##   ##
                     ##  ##   ##   ##
                 ##  ##  ##   ##   ##
          #####  ##  ## ##    #######
    ##   ##  ##  ##  ####     ##   ##
    ##   ######  ##  ## ##    ##   ##
    ##   ##  ##  ##  ##  ##   ##   ##
    #### ##  ##  ##  ##   ##  ##   ##
    """
    print(logo)
    print("Entering interactive mode.")
    print("Type 'exit' to quit.")
    print("Type 'help' for a list of commands.")


def interactive_loop():
    _print_welcome()

    commands = {
        'load': cmd_load,
        'add': cmd_add,
        'get': cmd_get,
        'list': cmd_list,
        'versions': None,  # Special handling
        'save': cmd_save,
        'load_project': cmd_load_project,
        'errors': cmd_errors,
        'help': cmd_help,
        'exit': None,  # Special handling
    }

    while True:
        try:
            user_input = input("\n>> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            match command:
                case 'versions':
                    sub_command = args[0].lower().strip() if args else ''
                    match sub_command:
                        case 'add':
                            cmd_versions_add(args[1:])
                        case 'get':
                            cmd_versions_get(args[1:])
                        case 'list':
                            cmd_versions_list(args[1:])
                        case _:
                            print(f"Unknown versions command: {sub_command}")
                case 'exit' | 'quit':
                    print("Exiting interactive mode.")
                    break
                case _:
                    if command in commands:
                        commands[command](args)
                    else:
                        print(f"Unknown command: {command}")
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break


def main():
    args = parse_args()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        if args.json_path:
            if os.path.isdir(args.json_path):
                storage = StorageJSON(args.json_path)
                lp.initialize(args.project_name, storage_backend=storage)
                print(f"Initialized project '{args.project_name}' "
                      f"with storage at '{args.json_path}'")
                lp.load()
            else:
                lp.initialize(args.project_name)
                report = lp.load_assets(args.json_path)
                print(f"Initialized project '{args.project_name}' ")
                if report['errors']:
                    print(f"{len(report['errors'])} errors during load")
        else:
            lp.initialize(args.project_name)
            print(f"Initialized project '{args.project_name}' ")

        interactive_loop()
    except KeyboardInterrupt:
        sys.exit(1)
