
import sys
import argparse
import signal
import os

import laika_pipeline as lp
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
        with open(filepath, 'r') as f:
            data = json.load(f)
        asset = lp.Asset(data['name'], data['type'])
        result = lp.add_asset(asset)
        if result['success']:
            print(f"Asset added: {asset.name} ({asset.asset_type.value})")
            print(f"Code: {result['asset_code']}")
        else:
            print(f"Failed to add asset: {result['error']}")
    except Exception as e:
        print(f"Error adding asset: {e}")


def cmd_get(args):
    # TODO
    pass


def cmd_list(args):
    # TODO
    pass


def cmd_versions_add(args):
    # TODO
    pass


def cmd_versions_get(args):
    # TODO
    pass

def cmd_versions_list(args):
    # TODO
    pass


def cmd_save(args):
    # TODO
    pass


def cmd_load_project(args):
    # TODO
    pass


def cmd_errors(args):
    # TODO
    pass


def cmd_help(args):
    help_text = """
    Available commands:
    load <file.json>                           Load assets from JSON file
    add <asset.json>                           Add a new asset from JSON file
    get <asset_name> <type>                    Get an asset by name and type
    list                                       List all assets
    versions add <asset_name> <version.json>   Add a version for an asset
    versions get <asset_name> <type> <version> Get a specific asset version
    versions list <asset_name> <type>          List all versions of an asset
    save                                       Save project to storage
    load_project                               Load project from storage
    errors                                     Show validation errors
    help                                       Show this help message
    exit                                       Exit the CLI
    """
    print(help_text)


def interactive_loop():
    print("Entering interactive mode. Type 'exit' to quit.")

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
                            cmd_versions_add(None)
                        case 'get':
                            cmd_versions_get(None)
                        case 'list':
                            cmd_versions_list(None)
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
