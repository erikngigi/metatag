"""CLI Schema and Input Validaition Module.

Acts as the View layer interface. Configures the argparse schema, enforces strict
positional argument ordering, and handles dynamic terminal completion hooks.

Usage:
    $ metatag tv "Breaking Bad" /downloads/raw /media/TV --videos-only -r
    $ metatag anime "Chainsaw Man" ./incoming ./anime --preview

Positionals:
    mode (str): ['anime', 'tv']. Sets regex rules and remote API targets.
    search_query (str): Title string used to query remote databases.
    target_dir (str): Path to the unorganized source files.
    output_dir (str): Path to the organized destination directory.

Options:
    --videos-only / --subtitles-only: Mutually exclusive file type filters.
    -r, --recursive / -nr, --non-recursive: Mutually exclusive folder depth toggles.
    -p, --preview: Safe dry-run mode; lists changes without altering files.
    --delete-old-files: Cleans up source directories post-execution.
"""

import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Configures the CLI argument schema and parses terminal inputs.
    """
    parser = argparse.ArgumentParser(
        prog="metatag",
        description="A structured, API-driven renaming engine that standardizes "
        "messy TV show and Anime file collections using remote metadata databases.",
    )

    # parser.add_argument("mode", choices=["anime", "tv"], help="The media type mode.")

    # parser.add_argument(
    #     "search_query", help="The explicit series name to query the API with (e.g., 'Naruto or 'Game of Thrones')."
    # )

    # ==============================================================================
    # OPTIONAL ARGUMENTS / FLAGS
    # ==============================================================================
    # io_group = parser.add_argument_group("Directory Configuration Options")
    # io_group.add_argument(
    #     "-d", "--target-dir", dest="target_dir", help="The source directory containing the media files to process."
    # )
    # io_group.add_argument(
    #     "-o", "--output-dir", dest="output_dir", help="The target output directory for processed files."
    # )
    #
    # filter_group = parser.add_mutually_exclusive_group()
    # filter_group.add_argument(
    #     "--videos-only", dest="videos_only", action="store_true", help="Only process video files (e.g., mp4, mkv)."
    # )
    # filter_group.add_argument(
    #     "--subtitles-only", dest="subtitles_only", action="store_true", help="Only process subtitle files (e.g., srt)."
    # )
    #
    # depth_group = parser.add_mutually_exclusive_group()
    # depth_group.add_argument(
    #     "-r", "--recursive", action="store_true", help="Scan the target directory and all subfolders recursively."
    # )
    # depth_group.add_argument(
    #     "-nr", "--non-recursive", action="store_true", help="Scan only the immediate top-level of the target directory."
    # )
    #
    # parser.add_argument(
    #     "-p",
    #     "--preview",
    #     action="store_true",
    #     dest="preview",
    #     help="Perform a dry run. Connects to API and prints proposed name changes without modifying any files.",
    # )
    parser.add_argument(
        "-a", "--interactive", action="store_true", help="Launch step-by-step interactive configuration setup wizard"
    )

    return parser.parse_args()
