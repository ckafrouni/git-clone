import os

from g import defaults
from g.objects import Tree, Blob


def read_index() -> Tree:
    """Read the index file."""

    with open(defaults.INDEX_FILE, "rb") as f:
        data = f.read()
    return Tree.deserialize(data)


def add(path: str) -> None:
    """Stage a file or directory."""

    # Read the index
    index = read_index()

    # We have a file, we want to add it to the index
    if os.path.isfile(path):
        add_file(index, path)

    # We have a directory, we want to add all files in it to the index, recursively, including the directory itself, which is a tree
    elif os.path.isdir(path):
        add_dir(index, path)

    else:
        print(f"Path {path} is not a file or directory.")
        return

    # Write the index
    index.write(defaults.INDEX_FILE)


def add_file(tree: Tree, path: str):
    """Add a file to the tree."""

    with open(path, "rb") as f:
        data = f.read()

    blob = Blob(data)

    basename = os.path.basename(path.strip("/").strip("\\"))
    tree.add_entry(blob.as_entry(basename))


def add_dir(parent_tree: Tree, path: str):
    """
    Add a directory to the index. This is a recursive operation.
    """

    # Create a new tree object specifically for this directory
    new_tree = Tree()

    # Loop through each file and subdirectory in the current directory
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        # If it's a file, add it to the current tree
        if os.path.isfile(file_path):
            add_file(new_tree, file_path)

        # If it's a directory, recursively add it and its contents to a new tree
        elif os.path.isdir(file_path):
            add_dir(new_tree, file_path)

    # Add an entry for the current tree to the parent index
    basename = os.path.basename(path.strip("/").strip("\\"))
    parent_tree.add_entry(new_tree.as_entry(basename))
