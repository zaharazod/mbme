import os, sys
from json import loads
from pathlib import Path
from typing import Any

from .attr_dict import AttrDict
from logging import getLogger, DEBUG, INFO, StreamHandler
logger = getLogger()
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))
log = logger.info


    
class ConfigFile(AttrDict):
    def __init__(self, path=None, data=None):
        super().__init__()
        if path:
            self.load(path)
        if data:
            self.update(data)

    def __getitem__(self, key):
        log(('cfg.getitem', key, type(key), '.' in key),)
        if isinstance(key, str) and '.' in key:  # TODO: regex match format?
            log('its a dotted string')
            part = self
            try:
                parts = key.split('.')
                while parts:
                    part_key = parts.pop(0)
                    part = part[part_key]
            except:
                return None
            return part
        return getattr(super(AttrDict, self), key)

    def loads(self, text):
        data = loads(text)
        self.update(data)

    def load(self, file_path):
        path = Path(file_path)
        self.loads(path.read_text())
        
    def apply_env(self):
        if 'env' in self and isinstance(self.env, dict):
            os.environ.update(self.env)
