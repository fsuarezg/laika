
import sys
import argparse
import signal

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
        help='Path to the project json file repository'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        if args.json_path:
            storage = StorageJSON(args.json_path)
            lp.initialize(args.project_name, storage_backend=storage)
            lp.load_assets(args.json_path)
        else:
            lp.initialize(args.project_name)
    except KeyboardInterrupt:
        sys.exit(1)
