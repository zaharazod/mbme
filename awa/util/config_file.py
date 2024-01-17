import os
import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict


# def path_to_str(p):
#     return p.as_posix() \
#         if callable(getattr(p, 'as_posix', None)) \
#         else p


class ConfigFile(MissingAttrDict):

    def __init__(self, data={}, *, path=None, env=True):
        super().__init__()
        if path:
            self.load(path)
        if data:
            self.update(data)
        if env:
            self.apply_env()

    def loads(self, text):
        data = loads(text)
        self.update(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())

    def apply_env(self):
        if issubclass(type(self.env), dict):
            os.environ.update(self.env)
