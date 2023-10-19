import hashlib
import zlib
import os

from g import defaults

class Blob:
    data: bytes
    hash: str

    def __init__(self, data: bytes):
        self.data = data
        self.hash = hashlib.sha1(data).hexdigest()

    def serialize(self) -> bytes:
        return self.data
    
    def write(self, path: str):
        with open(path, 'wb') as f:
            # f.write(zlib.compress(self.serialize()))
            f.write(self.serialize())

class Tree:
    class Entry:
        mode: str
        type: str
        hash: str
        name: str

        def __init__(self, mode:str, type: str, hash: str, name: str):
            self.name = name
            self.hash = hash
            self.type = type
            self.mode = mode

        def serialize(self) -> bytes:
            return f'{self.mode} {self.type} {self.hash}\t{self.name}'.encode()
        
    entries: list[Entry]
    hash: str

    def __init__(self, entries: list[Entry] = []):
        self.entries = entries
        self.hash = hashlib.sha1(self.serialize()).hexdigest()

    def serialize(self) -> bytes:
        return b'\n'.join([entry.serialize() for entry in self.entries])
    
    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        self.hash = hashlib.sha1(self.serialize()).hexdigest()

    def write(self, path: str):
        with open(path, 'wb') as f:
            # f.write(zlib.compress(self.serialize()))
            f.write(self.serialize())

    @staticmethod
    def deserialize(data: bytes) -> 'Tree':
        entries = []
        for line in data.split(b'\n'):
            if not line:
                continue
            mode, type, hash_and_name = line.split(b' ')
            hash, name = hash_and_name.split(b'\t')
            entries.append(Tree.Entry(mode.decode(), type.decode(), hash.decode(), name.decode()))
        return Tree(entries)