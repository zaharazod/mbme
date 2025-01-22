import os

# import sys
from json import loads
from pathlib import Path
from functools import reduce
from awa.util.debug import debug
from .attr_dict import MissingAttrDict, AttrDict


class ConfigFile(MissingAttrDict):
    _dict_class = MissingAttrDict

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


# The line `options = {}` is initializing an empty dictionary named `options`. This dictionary
# will be used to store and update various configuration options for the `EngineConfig` class.
class EngineConfig(AttrDict):
    _dict_class = AttrDict
    _backend_label = "BACKEND"
    _default_backend = None
    _default_type = None
    _backend_type_map = {}
    _default_options = {}

    def __init__(self, *args, base_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_path = base_path

        def got(x, y):
            return x or y in self

        if not reduce(got, ["type", self._backend_label], False):
            self.type = "default"
        self.transform()

    def transform(self):
        options = {}
        options.update(self._default_options)
        options.update(self)
        self.OPTIONS = dict(
            filter(
                lambda kv: not any(
                    [
                        kv[0].startswith("_"),
                        kv[0] in ("type", "OPTIONS", "BACKEND"),
                    ]
                ),
                options.items(),
            )
        )
        if self._backend_label not in self:
            backend_kls = self._backend_type_map.get(
                self.type or self._default_type, self._default_backend
            )
            self[self._backend_label] = backend_kls


class StorageConfig(EngineConfig):
    _default_type = "file"
    _backend_type_map = {
        # TODO: ? change to tuples or separate classes to
        # ## add/remove fields for each backend_type?
        "s3": "storages.backends.s3.S3Storage",
        "file": "django.core.files.storage.FileSystemStorage",
        "default": "django.core.files.storage.FileSystemStorage",
        "static": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }

    def __init__(self, *args, label=None, **kwargs):
        self._label = label if label else "default"
        self._default_options = {}
        super().__init__(*args, **kwargs)


class StaticConfig(StorageConfig):
    _default_type = "static"


class DatabaseConfig(EngineConfig):
    _default_backend = ""
    _default_options = {}


class AwaConfig(ConfigFile):
    _dict_class = MissingAttrDict
    _retype = {
        "storage": AttrDict,
        "constants": AttrDict,
    }

    # WIP: replace with TransformativeConfigs
    _templates = (
        # (
        #     "storage",
        #     lambda m, k: f"{m.upper()}_{k.upper()}",
        # ),
        (
            "connections",
            lambda m, k: f"SOCIAL_AUTH_{m.upper()}_{k.upper()}",
        ),
        # database ?
    )

    def __init__(self, *a, base_path=None, **kw):
        # self._base_path = (
        #     base_path
        #     if isinstance(base_path, Path)
        #     else (
        #         Path(base_path)
        #         if isinstance(base_path, str)
        #         else (
        #             Path(__file__).resolve().parent.parent.parent
        #             if base_path is True
        #             else None
        #         )
        #     )
        # )
        self._base_path = base_path
        print(f"{base_path} {type(base_path)}")
        print(f"{self._base_path} {type(self._base_path)}")
        super().__init__(data=self._defaults, *a, **kw)
        if self._base_path:
            self.load(self._base_path / "awa" / "defaults.json")
            self.load(self._base_path / "config" / "config.json")
            self.initialize()

    def get_current_project(self, request):
        projects = list([p for p in self.projects if request.site.domain in p.domains])
        return projects[0] if projects else None

    def initialize(self):
        self.init_defaults()
        self.init_storage()
        self.init_templates()
        self.init_env()
        self.init_projects()

    def init_projects(self):
        self.setdefault("projects", [])
        for project in self.projects:
            project.setdefault("domains", [])
            debug(type(project))
            debug(project.include_ip)
            if project.include_ip:
                import socket

                hostname = socket.gethostname()
                # FIXME path is uncertain here
                project.domains.append({"domain": "127.0.0.1", "path": "/"})
                for ip in socket.gethostbyname_ex(hostname)[2]:
                    project.domains.append({"domain": ip, "path": "/"})
                debug(project.domains)

    def init_defaults(self):
        for k, kls in self._retype.items():
            o = kls()
            if isinstance(self[k], dict):
                o.update(self[k])
            self[k] = o

    def init_storage(self):
        self.storages.setdefault("default", {})
        self.storages.setdefault("staticfiles", {})

        storages = {
            k: dict(v) for (k, v) in self.storages.items() if isinstance(v, dict)
        }
        defaults = {
            k: v
            for (k, v) in self.storages.items()
            if not isinstance(v, dict) and not k.startswith("_")
        }
        for k, v in storages.items():
            kls = StaticConfig if k.startswith("static") else StorageConfig
            vals = defaults.copy()
            vals.update(v)
            self.storages[k] = kls(vals, label=k)
        self.constants.STORAGES = dict(self.storages)

    def init_env(self):
        # set any environment variables from config
        if self.env and isinstance(self.env, dict):
            os.environ.update(self.env)

    def init_templates(self):
        # fill in some reasonable defaults (from defaults.json)
        # fills in self.constants with key/vals to set
        #   (eg. STATIC_URL, etc.)
        #
        # ..of course, now there's STORAGES...
        self.setdefault("constants", dict())
        for template_key, const_key_func in self._templates:
            items = self[template_key].items()
            template_items = list(filter(lambda zv: isinstance(zv[1], dict), items))
            defaults = list(filter(lambda zv: isinstance(zv[1], str), items))
            for cm, _ in template_items:
                for dk, dv in defaults:
                    self[template_key][cm].setdefault(dk, dv)
                    if r"%s" in self[template_key][cm][dk]:
                        self[template_key][cm][dk] = self[template_key][cm][dk] % cm
                    if dk == "root" and not self[template_key][cm][dk].startswith("/"):
                        self[template_key][cm][dk] = str(
                            self._base_path / self[template_key][cm][dk]
                        )
                    elif dk == "url":
                        url_parts = self[template_key][cm][dk].split(":/", 1)
                        url_path = url_parts.pop()
                        if not url_parts and not url_path.startswith("/"):
                            prefix = (
                                self.paths.prefix
                                if isinstance(self.paths.prefix, str)
                                and self.paths.prefix != "/"
                                else ""
                            )
                            self[template_key][cm][dk] = "/".join(
                                [prefix, self[template_key][cm][dk]]
                            )

                for dk in self[template_key][cm].keys():
                    if callable(const_key_func):
                        ck = const_key_func(cm, dk)
                        if ck:
                            self.constants.setdefault(ck, self[template_key][cm][dk])
