import os, sys
from json import loads
from pathlib import Path
from typing import Any
from .attr_dict import DottedAttrDict

class ConfigFile(DottedAttrDict):
    
    def __init__(self, path=None, data={}, env=True):
        super().__init__()
        if path:
            self.load(path)
        if data:
            self.update(data)
        if env:
            self.apply_env()

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except Exception as e:
            return None

    def loads(self, text):
        data = loads(text)
        self.update(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())

    def apply_env(self):
        if 'env' in self.__data__ and \
                isinstance(self.__data__['env'], dict):
            os.environ.update(self.env)
