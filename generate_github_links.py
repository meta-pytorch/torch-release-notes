#!/usr/bin/env python3
"""
Generate GitHub links for all .md files in a specified folder.
Output is formatted for easy import into Google Sheets.
"""

import argparse
import os
from pathlib import Path
from urllib.parse import quote


GITHUB_BASE_URL = "https://github.com/meta-pytorch/torch-release-notes/blob/main"


def generate_links(folder: str, output_file: str, use_hyperlink_formula: bool = False):
    """Generate GitHub links for all .md files in the folder."""
    folder_path = Path(folder)

    if not folder_path.exists():
        print(f"Error: Folder '{folder}' does not exist")
        return

    md_files = sorted(folder_path.glob("*.md"))

    if not md_files:
        print(f"No .md files found in '{folder}'")
        return

    with open(output_file, "w") as f:
        for md_file in md_files:
            # Get relative path from repo root
            relative_path = str(md_file)

            # URL encode the path (spaces -> %20, etc.)
            encoded_path = quote(relative_path)

            github_url = f"{GITHUB_BASE_URL}/{encoded_path}"

            if use_hyperlink_formula:
                # Google Sheets HYPERLINK formula format
                # Display name is the filename without path
                display_name = md_file.name
                f.write(f'=HYPERLINK("{github_url}", "{display_name}")\n')
            else:
                # Plain URL format (Google Sheets will auto-detect as link)
                f.write(f"{github_url}\n")

    print(f"Generated {len(md_files)} links in '{output_file}'")


def main():
    parser = argparse.ArgumentParser(
        description="Generate GitHub links for .md files in a folder"
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default="2.11.0/todo",
        help="Folder containing .md files (default: 2.11.0/todo)"
    )
    parser.add_argument(
        "-o", "--output",
        default="github_links.txt",
        help="Output file name (default: github_links.txt)"
    )
    parser.add_argument(
        "--formula",
        action="store_true",
        help="Use Google Sheets HYPERLINK formula format instead of plain URLs"
    )

    args = parser.parse_args()
    generate_links(args.folder, args.output, args.formula)


if __name__ == "__main__":
    main()
