import os
# import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict, is_dict


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


class ConfigFile(MissingAttrDict):

    def __init__(self, data=None, *a, path=None, **kw):
        super().__init__(*a, **kw)
        if path:
            self.load(path)
        if data:
            self.update(data)

    def loads(self, text):
        data = loads(text)
        self.update(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())


class AwaConfig(ConfigFile):
    def __init__(self, data=None, *a, base_path=None, process=True, **kw):
        self._base_path = Path(base_path) if base_path \
            else None  # Path(__file__).resolve().parent.parent.parent
        if data:
            a = (data, ) + a
        super().__init__(*a, **kw)
        # print(self, base_path, self._base_path, a, kw, sep=' ||| ')
        if self._base_path:
            self.load(self._base_path / 'awa' / 'defaults.json')
            self.load(self._base_path / 'config' / 'config.json')
            #  if process:
            #     self.process()

    def process(self):
        if is_dict(self.env) and self.env:
            os.environ.update(self.env.to_dict() \
                if callable(getattr(self.env, 'to_dict', False)) \
                else self.env)
