import os
from json import loads
from pathlib import Path
from typing import Any
from .attr_dict import AttrDict

class ConfigFile(AttrDict):
    def __init__(self, path=None, data=None):
        super().__init__()
        if path:
            self.load(path)
        if data:
            self.update(data)

    def __getitem__(self, k: Any) -> Any:
        if isinstance(k, str) and '.' in k:
            part = self
            try:
                parts = k.split('.')
                while parts:
                    part_key = parts.pop(0)
                    part = part[part_key]
            except:
                return None
            return part
        return super().__getitem__(k)

    def loads(self, text):
        data = loads(text)
        self.update(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())
        
    def apply_env(self):
        if 'env' in self and isinstance(self.env, dict):
            os.environ.update(self.env)
