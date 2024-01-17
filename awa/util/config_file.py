import os
import sys
from json import loads
from pathlib import Path
from .attr_dict import DottedAttrDict


class FalseChain:

    __call__ = __getitem__ = __getattr__ = lambda self, *a, **k: self
    def __repr__(_): return repr(False)
    def __str__(_): return str(False)
    def __bool__(self): return False


FALSE = FalseChain()


def path_check(p):
    return p.as_posix() \
        if callable(getattr(p, 'as_posix', None)) \
        else p


class ConfigFile(DottedAttrDict):

    def __init__(self, data={}, *, path=None, env=True):
        super().__init__()
        if path:
            path = path_check(path)
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
            os.environ.update(self.__data__['env'])
