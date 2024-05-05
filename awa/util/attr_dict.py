# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


def is_internal(key):
    return (
        isinstance(key, str)
        and key.isidentifier()
        and key.startswith("__")
    )


class AttrDict(dict):
    @property
    def _dict_class(self):
        return type(self)

    def __getitem__(self, key):
        try:
            if is_internal(key):
                value = getattr(self, key)
            else:
                value = super().__getitem__(key)
                value, changed = self._convert(value)
                if changed:
                    self[key] = value
        except Exception as e:
            raise e
        return value

    def __setitem__(self, key, value):
        if is_internal(key):
            return setattr(super(), key, value)
        value, _ = self._convert(value)
        super().__setitem__(key, value)
        return value

    def __getattr__(self, key):
        return (
            getattr(super(), key)
            if is_internal(key)
            else self.__getitem__(key)
        )

    def __setattr__(self, key, value):
        return (
            super().__setattr__(key, value)
            if is_internal(key)
            else self.__setitem__(key, value)
        )

    def _convert(self, val):
        try:
            kls = (
                val.get('_dict_class', None)
                if hasattr(val, 'get')
                and callable(val.get)
                else None
            ) or self._dict_class
            return (
                (kls(val), True)
                if isinstance(val, dict) and type(val) is not kls
                else (
                    (list([v for v, _ in map(self._convert, val)]), True)
                    if isinstance(val, list)
                    else (val, False)
                )
            )
        except Exception as e:
            print(val)
            raise (e)
            import sys
            sys.exit(0)

    def to_dict(self):
        d = dict(self)
        for k, v in d.items():
            if isinstance(v, AttrDict):  # or issubclass(type(v), AttrDict):
                d[k] = v.to_dict()
        return d

    def merge(self, other):
        kls = self._dict_class or type(self)
        for k, v in other.items():
            if all(map(lambda v: isinstance(v, dict), [self.get(k, None), v])):
                z = kls(self[k])
                z.merge(v)
                self[k] = z
            else:
                self[k] = v


class FalseChain(object):

    __getitem__ = __getattr__ = lambda s, *a, **k: s

    def __bool__(s):
        return False


FALSE = FalseChain()
DUMMY_VALUE = -23.005


class MissingAttrDict(AttrDict):
    def _replace(self, key):
        return isinstance(key, str) and key.isidentifier()

    def setdefault(self, k, dv):
        if k not in self or self[k] is FALSE:
            self[k] = dv

    def get(self, key, default=DUMMY_VALUE):
        try:
            return self.__getitem__(key)
        except KeyError as e:
            if default is not DUMMY_VALUE:
                return default
            raise e

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            if not self._replace(key):
                raise e
            return FALSE
