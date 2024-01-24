import os
# import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict


class FalseChain:

    __call__ = __getitem__ = __getattr__ = lambda self, *a, **k: self
    def __repr__(_): return repr(False)
    def __str__(_): return str(False)
    def __bool__(self): return False


FALSE = FalseChain()


class ConfigFile(MissingAttrDict):

    def __init__(self, data=None, *a, path=None, **kw):
        super().__init__(*a, **kw)
        if path:
            self.load(path)
        if data:
            self.merge(data)

    def loads(self, text):
        data = loads(text)
        self.merge(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())


class AwaConfig(ConfigFile):
    def __init__(self, data=None, *a, base_path=None, process=True, **kw):
        self._base_path = Path(base_path) if base_path \
            else None  # Path(__file__).resolve().parent.parent.parent
        super().__init__(data, *a, **kw)
        # print(self, base_path, self._base_path, a, kw, sep=' ||| ')
        if self._base_path:
            self.load(self._base_path / 'awa' / 'defaults.json')
            self.load(self._base_path / 'config' / 'config.json')
            if process:
                self.process()

    def process(self):
        if self.env and isinstance(self.env, dict):
            os.environ.update(self.env.to_dict()  # unclear if needed
                              if callable(self.env.to_dict)
                              else self.env)
