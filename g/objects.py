import hashlib
import os
from g import defaults

# import os
# import zlib
# from g import defaults


class Entry:
    mode: str
    type: str
    hash: str
    name: str
    content: "Tree | Blob"

    def __init__(
        self, mode: str, type: str, hash: str, name: str, content: "Tree | Blob"
    ):
        self.name = name
        self.hash = hash
        self.type = type
        self.mode = mode
        self.content = content

    def serialize(self) -> bytes:
        return f"{self.mode} {self.type} {self.hash} {self.name}".encode()


class Blob:
    data: bytes
    hash: str

    def __init__(self, data: bytes):
        self.data = data
        self.hash = hashlib.sha1(data).hexdigest()

    def serialize(self) -> bytes:
        return self.data

    def as_entry(self, name: str) -> Entry:
        return Entry(defaults.DEFAULT_FILE_MODE, defaults.BLOB, self.hash, name, self)

    def write(self, path: str):
        with open(path, "wb") as f:
            # f.write(zlib.compress(self.serialize()))
            f.write(self.serialize())


class Tree:
    entries: list[Entry]
    hash: str

    def __init__(self, entries: list[Entry] = []):
        self.entries = entries
        self.hash = hashlib.sha1(self.serialize()).hexdigest()

    def serialize(self) -> bytes:
        return b"\n".join([entry.serialize() for entry in self.entries])

    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        self.hash = hashlib.sha1(self.serialize()).hexdigest()

    def as_entry(self, name: str) -> Entry:
        return Entry(defaults.DEFAULT_DIR_MODE, defaults.TREE, self.hash, name, self)

    def write(self, path: str):
        with open(path, "wb") as f:
            # f.write(zlib.compress(self.serialize()))
            f.write(self.serialize())

    @staticmethod
    def deserialize(data: bytes) -> "Tree":
        tree = Tree()
        for line in data.split(b"\n"):
            if not line:
                continue
            mode, type, hash, name = line.decode().split(" ")

            if type == defaults.TREE:
                with open(os.path.join(defaults.GIT_DIR, "objects", hash), "rb") as f:
                    inner_data = f.read()
                sub_tree = Tree.deserialize(inner_data)
                tree.add_entry(Entry(mode, type, hash, name, sub_tree))
            elif type == defaults.BLOB:
                with open(os.path.join(defaults.GIT_DIR, "objects", hash), "rb") as f:
                    inner_data = f.read()
                blob = Blob(inner_data)
                tree.add_entry(Entry(mode, type, hash, name, blob))
            else:
                raise ValueError(f"Unknown type {type}")

        return tree
