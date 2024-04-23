import os

# import sys
from json import loads
from pathlib import Path
from .attr_dict import MissingAttrDict


class FalseChain:

    __call__ = __getitem__ = __getattr__ = lambda self, *a, **k: self

    def __repr__(_):
        return repr(False)

    def __str__(_):
        return str(False)

    def __bool__(self):
        return False


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
        (
            "storage",
            lambda m, k: f"{m.upper()}_{k.upper()}",
        ),
        (
            "connections",
            lambda m, k: f"SOCIAL_AUTH_{m.upper()}_{k.upper()}",
        ),
        # database ?
    )

    def __init__(self, *a, base_path=None, **kw):
        self._base_path = (
            base_path
            if isinstance(base_path, Path)
            else (
                Path(base_path)
                if isinstance(base_path, str)
                else (
                    Path(__file__).resolve().parent.parent.parent
                    if base_path is True
                    else None
                )
            )
        )
        super().__init__(*a, **kw)
        if self._base_path:
            self.load(self._base_path / "awa" / "defaults.json")
            self.load(self._base_path / "config" / "config.json")
            self.initialize()

    def get_current_project(self, request):
        projects = list(
            [p for p in self.projects
                if request.site.domain in p.domains])
        return projects[0] if projects else None

    def initialize(self):
        self.init_templates()
        self.init_env()
        self.init_projects()

    def init_projects(self):
        self.setdefault('projects', [])
        for project in self.projects:
            project.setdefault('domains', [])
            if project.include_ip:
                import socket
                hostname = socket.gethostname()
                for ip in socket.gethostbyname_ex(hostname)[2]:
                    project.domains.append(ip)

    def init_env(self):
        # set any environment variables from config
        if self.env and isinstance(self.env, dict):
            os.environ.update(
                self.env.to_dict()  # unclear if needed
                if callable(self.env.to_dict)
                else self.env
            )

    def init_templates(self):
        # fill in some reasonable defaults (from defaults.json)
        # fills in self.constants with key/vals to set
        #   (eg. STATIC_URL, etc.)
        self.setdefault("constants", dict())
        for template_key, const_key_func in self._templates:
            items = self[template_key].items()
            template_items = list(
                filter(lambda zv: isinstance(zv[1], dict), items))
            defaults = list(filter(lambda zv: isinstance(zv[1], str), items))
            for cm, _ in template_items:
                for dk, dv in defaults:
                    self[template_key][cm].setdefault(dk, dv)
                    if r"%s" in self[template_key][cm][dk]:
                        self[template_key][cm][dk] = self[template_key][cm][dk] % cm
                    if dk == "root" and \
                            not self[template_key][cm][dk].startswith("/"):
                        self[template_key][cm][dk] = str(
                            self._base_path / self[template_key][cm][dk])
                    elif dk == "url":
                        url_parts = self[template_key][cm][dk].split(':/', 1)
                        url_path = url_parts.pop()
                        if not url_parts and not url_path.startswith('/'):
                            prefix = self.paths.prefix \
                                if isinstance(self.paths.prefix, str) \
                                and self.paths.prefix != '/' \
                                else ''
                            self[template_key][cm][dk] = '/'.join([
                                prefix,
                                self[template_key][cm][dk]
                            ])

                for dk in self[template_key][cm].keys():
                    if callable(const_key_func):
                        ck = const_key_func(cm, dk)
                        if ck:
                            self.constants.setdefault(
                                ck, self[template_key][cm][dk])
