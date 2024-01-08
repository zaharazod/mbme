import os
import sys
from json import loads
from pathlib import Path
from .attr_dict import DottedAttrDict


class FalseChain:

    __call__ = __getitem__ = __getattr__ = lambda self, *a, **k: self
    def __bool__(self): return False


FALSE = FalseChain()


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
        except Exception:
            return FALSE

    __getattr__ = __getitem__

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
