import os

from g import defaults


def g_init(path: str = "."):
    """
    Initialize a new repository.
    See g/defaults.py for the default directory structure.

    :param path: The path to the repository.
    """
    # Create the path if it doesn't exist
    if not os.path.exists(path):
        os.mkdir(path)

    # Create the .g directory
    if os.path.exists(os.path.join(path, defaults.GIT_DIR)):
        raise Exception("Repository already exists.")
    os.mkdir(os.path.join(path, defaults.GIT_DIR))

    # Create the index file
    open(os.path.join(path, defaults.INDEX_FILE), "w").close()

    # Create the objects directory
    os.mkdir(os.path.join(path, defaults.OBJ_DIR))

    # Create the refs directory
    os.mkdir(os.path.join(path, defaults.REFS_DIR))

    # Create the HEAD file
    open(os.path.join(path, defaults.HEAD_FILE), "w").close()

    # Create the main branch
    with open(os.path.join(path, defaults.HEAD_FILE), "w") as f:
        f.write("ref: refs/heads/main\n")
