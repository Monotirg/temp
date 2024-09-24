from __future__ import annotations

import os
import json

from dataclasses import dataclass
from typing import List, Dict, Iterator



@dataclass
class NodeFile:
    name: str
    path: str

    def to_json(self) -> Dict:
        return {
            "type": "file",
            "name": self.name,
            "path": self.path
        }

@dataclass
class NodeDir:
    name: str
    path: str
    files: List[NodeFile]
    dirs: List[NodeDir]

    def to_json(self) -> Dict:
        return {
            "type": "dir",
            "name": self.name,
            "path": self.path, 
            "child": [
                item.to_json() 
                for item in self.files + self.dirs
            ]
        }


class Tree:
    def __init__(self, root: str) -> None:
        path = os.path.normpath(root)
        name = os.path.basename(root)
        self.prefix = os.path.dirname(root)
        self.root = NodeDir(name, path, [], [])
        self.mapper = {path: self.root}
        
    @classmethod
    def load_dir(cls, root: str) -> Tree:
        tree = cls(root)
        
        for path in tree._iter_files():
            if os.path.isfile(path):
                tree._add_file(path)
            else:
                tree._add_dir(path)
        
        return tree
    
    def to_json(self) -> str:
        return json.dumps(self.root.to_json(), indent=2)
        
 
    def _iter_files(self) -> Iterator[str]:
        for path, dirs, files in os.walk(self.root.path):
            for file in files:
                yield os.path.join(path, file)

            if not (files or dirs):
                yield path

    def _add_file(self, path: str) -> None:
        subdir = os.path.dirname(path)
        self._add_dir(subdir)
            
        subdir_node = self.mapper[subdir]
        subdir_node.files.append(NodeFile(
            name=os.path.basename(path),
            path=path
        ))

    def _add_dir(self, path: str) -> None:
        subdirs = []

        while path not in self.mapper:
            subdirs.append(os.path.join(self.prefix, path))
            path = os.path.dirname(path)
            
        start = self.mapper[path]

        for subdir in subdirs:
            subdir_node = NodeDir(
                name=os.path.basename(subdir),
                path=subdir,
                files=[],
                dirs=[]
            )
            self.mapper[subdir] = subdir_node
            start.dirs.append(subdir_node)
            start = subdir_node 
    
    def __show(self, node_dir, indent) -> None:
        print(" " * indent + node_dir.name)
        indent += 4 

        for file in node_dir.files:
            print(" " * indent + file.name)
        
        for dir in node_dir.dirs:
            self.__show(dir, indent)

    def show(self) -> None:
        self.__show(self.root, 0) 
