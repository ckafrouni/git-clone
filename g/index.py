import os

from g import objects, defaults

def read_index() -> objects.Tree:
    """Read the index file."""
    with open(defaults.INDEX_FILE, 'rb') as f:
        data = f.read()
    return objects.Tree.deserialize(data)


def add(path: str):
    """Stage a file or directory."""
    # Read the index
    index = read_index()
    print(index.serialize())

    # We have a file, we want to add it to the index
    if os.path.isfile(path):
        add_file(index, path)

    # We have a directory, we want to add all files in it to the index, recursively, including the directory itself, which is a tree
    elif os.path.isdir(path):
        add_dir(index, path)

    else:
        raise Exception('Not a file or directory.')

def add_file(index: objects.Tree, path: str):
    """Add a file to the index."""
    if not os.path.isfile(path):
        raise Exception('Not a file.')
    
    with open(path, 'rb') as f:
        data = f.read()

    blob = objects.Blob(data)
    blob.write(os.path.join(defaults.OBJ_DIR, blob.hash))

    basename = os.path.basename(path.strip('/'))
    entry = objects.Tree.Entry(defaults.DEFAULT_FILE_MODE, defaults.BLOB, blob.hash, basename)

    index.add_entry(entry)
    index.write(defaults.INDEX_FILE)

def add_dir(parent_index: objects.Tree, path: str):
    """
    Add a directory to the index. This is a recursive operation.
    """
    if not os.path.isdir(path):
        raise Exception('Not a directory.')
    
    # Create a new tree object specifically for this directory
    current_tree = objects.Tree()
    
    # Loop through each file and subdirectory in the current directory
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        
        # If it's a file, add it to the current tree
        if os.path.isfile(file_path):
            add_file(current_tree, file_path)
        
        # If it's a directory, recursively add it and its contents to a new tree
        elif os.path.isdir(file_path):
            add_dir(current_tree, file_path)
    
    # Serialize the current tree and write it to disk
    current_tree.write(os.path.join(defaults.OBJ_DIR, current_tree.hash))
    
    # Add an entry for the current tree to the parent index
    basename = os.path.basename(path)
    entry = objects.Tree.Entry(defaults.DEFAULT_DIR_MODE, defaults.TREE, current_tree.hash, basename)
    parent_index.add_entry(entry)
    parent_index.write(defaults.INDEX_FILE)
