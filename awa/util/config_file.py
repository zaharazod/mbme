import os
import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict, is_dict, EphemeralAttrDict


class ConfigFile(MissingAttrDict):

    def __init__(self, data=None, *a, path=None, env=False, **kw):
        super().__init__(*a, **kw)
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
        if is_dict(self.env) and self.env:
            print(self.env, bool(self.env))
            sys.exit()
            os.environ.update(self.env)
