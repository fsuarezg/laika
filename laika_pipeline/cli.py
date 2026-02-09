
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


def interactive_loop():
    print("Entering interactive mode. Type 'exit' to quit.")
    while True:
        try:
            command = input(">> ")
            if command.lower() in ['exit', 'quit']:
                print("Exiting interactive mode.")
                break
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
