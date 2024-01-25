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
    _templates = (
        ('storage', lambda m, k: f'{m.upper()}_{k.upper()}',),
        ('connections', lambda m, k: f'SOCIAL_AUTH_{m.upper()}_{k.upper()}',),
        # database ?
    )

    def __init__(self, data=None, *a, base_path=None, **kw):
        self._base_path = \
            base_path if isinstance(base_path, Path) else \
            Path(base_path) if isinstance(base_path, str) else \
            Path(__file__).resolve().parent.parent.parent if base_path is True else \
            None
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
        for key, const_key_func in self._templates:
            items = self[key].items()
            template_items = list(filter(
                lambda zv: isinstance(zv[1], dict), items))
            defaults = list(filter(
                lambda zv: isinstance(zv[1], str), items))
            for cm, _ in template_items:
                for dk, dv in defaults:
                    self[key][cm].setdefault(dk, dv)
                    if r'%s' in self[key][cm][dk]:
                        self[key][cm][dk] = self[key][cm][dk] % cm
                    if dk == 'root' and not self[key][cm][dk].startswith('/'):
                        self[key][cm][dk] = str(
                            self._base_path / self[key][cm][dk])
                for dk in self[key][cm].keys():
                    if callable(const_key_func):
                        ck = const_key_func(cm, dk)
                        if ck:
                            self.constants.setdefault(ck, self[key][cm][dk])
