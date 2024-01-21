# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


def is_internal(key): return isinstance(key, str) and key.startswith('__')
def is_dotted(key): return isinstance(key, str) and '.' in key
def is_a(o, t): return issubclass(type(o), t)
def is_dict(o): return is_a(o, (dict, AttrDict))


class AttrDict(dict):

    @classmethod
    def _convert(cls, val):
        return (cls(val), True) \
            if isinstance(val, dict) \
            else (val, False)

    def to_dict(self):
        d = dict(self)
        for k, v in d.items():
            if is_a(v, AttrDict):
                d[k] = v.to_dict()
        return d

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()})'

    def __getitem__(self, key):
        try:
            if is_a(key, str) and key in self.__dict__:
                value = getattr(self, key)
            else:
                value = super().__getitem__(key)
                value, changed = type(self)._convert(value)
                if changed:
                    self[key] = value
        except Exception as e:
            raise e
        return value

    def __setitem__(self, key, value):
        if is_internal(key):
            return super().__setattr__(key, value)

        value, _ = type(self)._convert(value)
        super().__setitem__(key, value)
        return value

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        return super().__setattr__(key, value) \
            if is_internal(key) \
            else self.__setitem__(key, value)

    def update(self, other=None):
        if not other:
            return
        if is_dict(other):
            other = other.items()
        for k, v in other:
            if isinstance(v, dict):
                v = type(self)(v)
            self[k] = v


class DottedAttrDict(AttrDict):

    def __getitem__(self, key):
        if is_dotted(key):
            parts = key.split('.')
            return self.__getitem__(parts.pop(0))['.'.join(parts)]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if is_internal(key):
            return super().__setitem__(key, value)
        if is_dotted(key):
            parts = key.split('.')
            key = parts.pop(0)
            new_path = '.'.join(parts)
            self[key] = type(self)()
            return super(type(self[key]), self[key]).__setitem__(new_path, value)
        return super().__setitem__(key, value)


class FalseChain(object):

    __getitem__ = __getattr__ = lambda s, *a, **k: s
    def __bool__(s): return False


FALSE = FalseChain()
DUMMY_VALUE = -23.005


class MissingAttrDict(AttrDict):
    def _replace(self, key):
        import re
        return is_a(key, str) \
            and re.match(r'^[a-zA-Z_]+$', key)

    def get(self, key, default=DUMMY_VALUE):
        try:
            v = super().__getitem__(key)
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
            v = type(self)()
            self.__dict__[key] = v

    def __getattr__(self, key):
        return getattr(super(), key) \
            if is_internal(key) \
            else self.__getitem__(key)
