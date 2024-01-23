import os
# import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict, is_dict


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
            os.environ.update(self.env.to_dict())
