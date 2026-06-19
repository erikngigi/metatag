import argparse
import sys
from pathlib import Path
from typing import Any

# Set up main parser
parser = argparse.ArgumentParser(description="TV Show File Scanner and Renamer.")

# Argument 1: The target directory (Stores a string in 'target_dir')
# parser.add_argument("-d", "--dir", dest="target_dir", required=True, help="The target directory to scan.")
parser.add_argument("target_dir", help="The target directory to scan.")

# Depth options (mutually exclusive)
depth_group = parser.add_mutually_exclusive_group()
depth_group.add_argument(
    "-r", "--recursive", action="store_true", default="/storage/Tv-Shows", dest="recursive", help="Scan recursively."
)
depth_group.add_argument("-nr", "--non-recursive", action="store_true", dest="nr_recursive", help="Scan top-level.")

# Filter options (mutually exclusive)
filter_group = parser.add_mutually_exclusive_group()
filter_group.add_argument("--videos-only", action="store_true", help="Filter for video files only.")
filter_group.add_argument("--subs-only", action="store_true", help="Filter for subtitle files only.")

args: argparse.Namespace = parser.parse_args()

# Validate the directory
dir_path = Path(args.target_dir)

if not dir_path.exists() or not dir_path.is_dir():
    print(f"Error: '{args.target_dir}' is not a valid directory", file=sys.stderr)
    sys.exit(1)

# Determine which extensions are allowed based on the flags
if args.videos_only:
    allowed_extensions = {"mp4", "mkv"}
elif args.subs_only:
    allowed_extensions = {"srt"}
else:
    allowed_extensions = {"mp4", "mkv", "srt"}

# Choose the pathlib tool based on the depth flags
# (Defaults to non-recursive if they don't specify)
search_generator = dir_path.rglob("*") if args.recursive else dir_path.glob("*")

files: list[Any] = []

for item in search_generator:
    if item.is_file() and item.suffix.lower().lstrip(".") in allowed_extensions:
        files.append(item)

if not files:
    print("No matching files found based on your filters.")
else:
    for file in files:
        if args.recursive:
            print(f"[R] {file.relative_to(dir_path)}")
        else:
            print(f"NR {file.name}")
