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

    # never tell an engineer something is over-engineered
    #
    # i'll engineer even harder
    _templates = ('storage',)
    _constant_templates = (
        lambda m, k: f'{m.upper()}_{k.upper()}',
    )

    def __init__(self, data=None, *a, base_path=None, **kw):
        self._base_path = Path(base_path) if base_path \
            else None  # Path(__file__).resolve().parent.parent.parent
        super().__init__(data, *a, **kw)
        if self._base_path:
            self.load(self._base_path / 'awa' / 'defaults.json')
            self.load(self._base_path / 'config' / 'config.json')
            self.initialize()

    def initialize(self):
        self.init_templates()
        self.init_env()

    def init_env(self):
        # set any environment variables from config
        if self.env and isinstance(self.env, dict):
            os.environ.update(self.env.to_dict()  # unclear if needed
                            if callable(self.env.to_dict)
                            else self.env)

    def init_templates(self):
        # fill in some reasonable defaults (from defaults.json)
        # fills in self.constants with key/vals to set
        #   (eg. STATIC_URL, etc.)
        self.setdefault('constants', dict())
        for key in self._templates:
            items = self[key].items()
            template_items = list(filter(lambda zv: isinstance(zv[1], dict), items))
            defaults = list(filter(lambda zv: isinstance(zv[1], str), items))
            for k, _ in template_items:
                for dk, dv in defaults:
                    self[key][k].setdefault(dk, dv)
                    if r'%s' in self[key][k][dk]:
                        self[key][k][dk] = self[key][k][dk] % k
                    if dk == 'root' and not self[key][k][dk].startswith('/'):
                        self[key][k][dk] = str(self._base_path / self[key][k][dk])
                    for cfunc in self._constant_templates:
                        ck = cfunc(k, dk)
                        if ck:
                            self.constants.setdefault(ck, self[key][k][dk])
        
        
