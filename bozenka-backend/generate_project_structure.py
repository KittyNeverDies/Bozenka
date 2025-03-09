# generate_readme.py

import os
from pathlib import Path

def get_project_tree(directory='.', exclude_dirs=None, prefix=''):
    """Generate a tree-like structure of the project directory."""
    if exclude_dirs is None:
        exclude_dirs = {'.git', '.idea', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv', '.env', 'node_modules'}

    # Get the project name from the current directory
    project_name = os.path.basename(os.path.abspath(directory))

    # Initialize the tree with the project name and root directory
    tree = [f"## {project_name}\n\n{project_name}/"]

    def walk_directory(current_path, prefix=''):
        entries = sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name.lower()))
        entries_count = len(entries)

        for idx, entry in enumerate(entries):
            is_last = idx == entries_count - 1

            # Skip excluded directories and their contents
            if entry.is_dir() and entry.name in exclude_dirs:
                continue

            # Create the appropriate prefix for the current item
            current_prefix = '└── ' if is_last else '├── '

            # Add the entry to the tree
            if not entry.is_dir():
                tree.append(f"{prefix}{current_prefix}{entry.name}")

            # If it's a directory, process its contents
            if entry.is_dir():
                tree.append(f"{prefix}{current_prefix}{entry.name}/")
                next_prefix = prefix + ('    ' if is_last else '│   ')
                walk_directory(entry.path, next_prefix)

    # Start walking from the root directory
    walk_directory(directory)

    return '\n'.join(tree)

def generate_readme():
    """Generate README.md content with the project structure."""
    # Get the project tree structure
    project_structure = get_project_tree()
    print(project_structure)
    # Create README content with project tree
    readme_content = "# Project Structure\n\n"
    readme_content += "The following is the basic structure of this project:\n\n"
    readme_content += "```\n"
    readme_content += project_structure
    readme_content += "\n```\n\n"

    # Write content to README.md


    print("README.md has been generated successfully!")

if __name__ == "__main__":
    generate_readme()
