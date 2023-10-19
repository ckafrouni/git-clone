from os import path

# Object types
BLOB = "blob"
TREE = "tree"
COMMIT = "commit"

# Default directory structure
GIT_DIR = ".g"
OBJ_DIR = path.join(GIT_DIR, "objects")
REFS_DIR = path.join(GIT_DIR, "refs")
INDEX_FILE = path.join(GIT_DIR, "index")
HEAD_FILE = path.join(GIT_DIR, "HEAD")

# Default branch
MAIN_BRANCH = "main"

# Default mode
DEFAULT_FILE_MODE = "100644"
DEFAULT_DIR_MODE = "040000"

# Default author
DEFAULT_AUTHOR = "<anonymous>"
DEFAULT_EMAIL = "<anonymous>"
