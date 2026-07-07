# Metatag

**A production-grade CLI asset organizer for automated media metadata lookup and batch file renaming.**

`metatag` bridges your local media library with industry-standard metadata databases — [TVMaze](https://www.tvmaze.com/api) and [Jikan (MyAnimeList)](https://jikan.moe/) — to eliminate manual file renaming. It identifies your media, fetches accurate episode metadata, and renames your files to a clean, consistent, industry-standard format, all through an interactive terminal experience.

---

## Table of Contents

- [Features](#features)
- [Naming Conventions](#naming-conventions)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [CLI Flags Reference](#cli-flags-reference)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Features

- **Dual API Integration** — Automatically queries the **TVMaze API** for western TV shows and the **Jikan API** for anime, so you get the correct source depending on content type.
- **Interactive TUI** — Powered by `InquirerPy`, allowing you to search, browse, and select the correct title/episode match using arrow-key navigation directly in your terminal — no manual ID lookups required.
- **Strict Format Normalization** — Parses local filenames and renames them to a precise, consistent convention depending on media type (see below).
- **Granular Execution Control** — A robust `argparse`-driven CLI supports targeted directory scans, media-type-specific scraping modes, and a `--dry-run` simulation mode so you can preview changes before committing to them.
- **Safe by Default** — Renaming operations are non-destructive; files are renamed in place and no metadata or file content is modified.

---

## Naming Conventions

| Media Type   | Format                                             | Example                                                      |
| ------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| **TV Shows** | `[Show Name] S[Season]E[Episode] - [Episode Name]` | `X-Men 97 S02E01 - Days of the Future Past.mkv`              |
| **Anime**    | `[Anime Name] [Episode Number] - [Episode Name]`   | `Legend of the Galactic Heroes 055 - After the Ceremony.mkv` |

> File extensions are always preserved from the original source file.

---

## Tech Stack

| Component             | Technology                                                   |
| --------------------- | ------------------------------------------------------------ |
| Language              | Python 3.10+                                                 |
| HTTP Client           | `requests`                                                   |
| Interactive Prompts   | `InquirerPy`                                                 |
| CLI Argument Parsing  | `argparse`                                                   |
| TV Metadata Source    | [TVMaze REST API](https://www.tvmaze.com/api)                |
| Anime Metadata Source | [Jikan API](https://jikan.moe/) (unofficial MyAnimeList API) |
| Dependency Management | `uv` / `pip`                                                 |

---

## Prerequisites

Before installing, ensure you have:

- **Python 3.10 or higher** installed (`python3 --version`)
- **pip** or [**uv**](https://github.com/astral-sh/uv) for dependency management
- An active internet connection (required for API metadata lookups)

No API keys are required — both TVMaze and Jikan expose public, unauthenticated endpoints.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/metatag.git
cd metatag
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

Using `pip`:

```bash
pip install -r requirements.txt
```

Using `uv` (recommended, respects `uv.lock` for reproducible installs):

```bash
uv sync
```

### 4. Verify the installation

```bash
python -m metatag.main --help
```

You should see the CLI's help output listing available flags.

---

## Usage

### Basic interactive run

Launch the interactive TUI to match and rename files:

```bash
python -m metatag.main -a
```

<!-- ### Specify media type explicitly -->
<!---->
<!-- ```bash -->
<!-- # TV show mode -->
<!-- python -m metatag.main --path ./Downloads/Shows --mode tv -->
<!---->
<!-- # Anime mode -->
<!-- python -m metatag.main --path ./Downloads/Anime --mode anime -->
<!-- ``` -->

### Preview changes without renaming (dry run)

```bash
python -m metatag.main -a -d
```

### Typical workflow

1. Run the CLI against a target directory.
2. Select **TV** or **Anime** mode (or let the tool infer it, depending on configuration).
3. Search for the show/anime title when prompted.
4. Use arrow keys to select the correct match from the returned results.
5. Confirm the proposed renaming plan.
6. Files are renamed in place according to the [naming conventions](#naming-conventions) above.

---

## CLI Flags Reference

| Flag                 | Description                                                                                | Required |
| -------------------- | ------------------------------------------------------------------------------------------ | -------- |
| `--path <dir>`       | Target directory containing media files to scan and rename.                                | Yes      |
| `--mode <tv\|anime>` | Explicitly selects the scraping/metadata mode.                                             | No       |
| `--dry-run`          | Simulates the renaming process and prints the intended changes without touching any files. | No       |
| `--help`             | Displays usage information and available flags.                                            | No       |

> Run `python -m metatag.main --help` at any time for the authoritative, up-to-date flag list.

---

## Project Structure

```text
.
├── metatag
│   ├── __init__.py
│   ├── cli.py                   # Argument parsing entry point (argparse config, flag definitions)
│   ├── colors.py                 # Terminal output styling/color constants for TUI readability
│   ├── controllers               # Core business logic layer
│   │   ├── __init__.py
│   │   ├── anime/                # Anime-specific controller logic (Jikan API orchestration)
│   │   ├── shared/                # Shared logic reused across TV/anime flows (e.g. file I/O, renaming)
│   │   ├── tv/                    # TV-specific controller logic (TVMaze API orchestration)
│   │   └── workflow_router.py     # Routes execution to the correct controller based on --mode
│   ├── main.py                   # Application entry point (invoked via `python -m metatag.main`)
│   ├── models                    # Data layer: API response schemas and typed models
│   │   ├── __init__.py
│   │   ├── anime_model.py        # Data model representing Jikan/anime API responses
│   │   ├── schemas/               # Shared schema/validation definitions
│   │   └── tvmaze_model.py       # Data model representing TVMaze API responses
│   └── views                     # Presentation layer: interactive terminal prompts
│       ├── __init__.py
│       ├── anime_menu.py         # InquirerPy menu for anime search/selection
│       ├── base_menu.py          # Shared base class for common menu behavior
│       └── tv_menu.py            # InquirerPy menu for TV show search/selection
├── metatag.spec                  # PyInstaller build spec (for packaging standalone binaries)
├── pyproject.toml                # Project metadata and dependency declarations
├── README.md                     # This file
├── requirements.txt               # Pip-compatible dependency list
└── uv.lock                       # Locked dependency versions for reproducible `uv` installs
```

---

## Architecture Overview

The application follows a lightweight **MVC-inspired layering**:

- **`views/`** — Handles all user-facing interaction via `InquirerPy` prompts (search input, result selection, confirmation).
- **`controllers/`** — Owns the business logic: calling the appropriate API client, mapping results to file operations, and performing the actual rename. Split into `tv/`, `anime/`, and `shared/` to keep media-type-specific logic isolated while reusing common utilities.
- **`models/`** — Defines typed representations of API responses (`tvmaze_model.py`, `anime_model.py`) and shared schema validation, decoupling the rest of the app from raw API payloads.
- **`workflow_router.py`** — The dispatch point that determines, based on `--mode` (or inferred context), which controller pipeline (`tv` or `anime`) handles the current run.
- **`cli.py` / `main.py`** — The composition root: parses arguments and wires the router, controllers, and views together at runtime.

This separation keeps API integration, file-system side effects, and terminal UI concerns independent, making it straightforward to add a new media source (e.g. a movie database) without touching existing TV/anime logic.

---

## Development

### Building a standalone binary

The repository includes a `metatag.spec` file for [PyInstaller](https://pyinstaller.org/):

```bash
pyinstaller metatag.spec
```

The compiled binary will be output to the `dist/` directory.

### Adding a new metadata source

1. Add a new model in `metatag/models/` describing the API's response shape.
2. Add a new controller package under `metatag/controllers/` (mirroring `tv/` or `anime/`).
3. Add a corresponding view under `metatag/views/` for the interactive selection prompt.
4. Register the new mode in `workflow_router.py` and expose it via a new `--mode` choice in `cli.py`.

---

## Troubleshooting

| Issue                     | Likely Cause                                      | Resolution                                                     |
| ------------------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| `No results found` in TUI | Title mismatch or overly specific search term     | Try a shorter or alternate title spelling                      |
| Rename does not apply     | Ran with `--dry-run`                              | Remove the `--dry-run` flag to apply changes                   |
| API request errors        | Network connectivity or upstream API downtime     | Verify internet access; retry after a short delay              |
| Files skipped silently    | Unsupported file extension or unparsable filename | Ensure source filenames contain identifiable show/episode info |

---

## Contributing

1. Fork the repository and create a feature branch.
2. Keep changes scoped to a single controller/view/model where possible.
3. Ensure new media-type integrations follow the existing `controllers/<type>/`, `models/<type>_model.py`, `views/<type>_menu.py` pattern.
4. Submit a pull request with a clear description of the change and, where applicable, a `--dry-run` output sample demonstrating the new behavior.
