# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
from re import match

def is_internal(k): return isinstance(k, str) and k.startswith('__')
def is_dotted(k): return isinstance(k, str) and '.' in k
def is_a(o, t): return issubclass(type(o), t)
def is_dict(o): return is_a(o, (dict, AttrDict))
def is_attr(k): return is_a(k, str) and match(r'^[a-zA-Z_]+$', k)


class AttrDict(dict):

    @classmethod
    def _check_type(cls, val):
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
                return value
            value = super().__getitem__(key)
            value, changed = type(self)._check_type(value)
            if changed:
                self[key] = value
        except Exception as e:
            raise e
        return value

    def __setitem__(self, key, value):
        if is_internal(key):
            return super().__setattr__(key, value)

        value, _ = type(self)._check_type(value)
        super().__setitem__(key, value)
        return value

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        if is_internal(key):
            return super().__setattr__(key, value)

        return self.__setitem__(key, value)

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
    __getitem__ = __getattr__ = lambda s, *_: s
    def __bool__(_): return False
    def __call__(s, *_, **__): return s


FALSE = FalseChain()


class EphemeralChain(object):
    def __init__(self, obj, key, t=None, *_, **__):
        self._target = obj
        self._target_keys = [key]
        self._target_type = t \
            or getattr(self, '_target_type', False) \
            or type(obj)  # or {} ?
        self._target_replaced = False

    def _check_valid(self):
        if self._target_replaced:
            raise TypeError('ephemeral instance no longer valid')

    def __getitem__(self, key):
        print('get', key)
        self._check_valid()
        self._target_keys.append(key)
        return self

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __bool__(self):
        self._check_valid()
        return False

    def __setitem__(self, key, value):
        # this may have esoteric bugs
        # ie. x=a.b.c; a.b.c.d = 3; x.y = 5; a.b.c.y == ??; x== ??
        self._check_valid()
        self._target_keys.append(key)
        keys = self._target_keys.copy()
        obj = self._target
        while keys:
            k = keys.pop(0)
            obj[k] = self._target_type() \
                if keys else value
            obj = obj[k]
        self._target_replaced = True

    def __setattr__(self, key, value):
        if is_internal(key):
            super().__setitem__(key, value)
        else:
            self.__setitem__(key, value)


DUMMY_VALUE = -23.00523


class MissingAttrDict(AttrDict):
    def __init__(self, *a, replacement=None, **kw):
        self._replacement = replacement \
            or getattr(type(self), '_replacement', False) \
            or type(self)
        super().__init__(*a, **kw)

    def _replace(self, key):
        from re import match
        return is_a(key, str) \
            and match(r'^[a-zA-Z_]+$', key)

    def get(self, key, default=DUMMY_VALUE):
        try:
            v = super().__getitem__(key)
        except KeyError as e:
            if default is DUMMY_VALUE:
                raise e
            v = default
            self[key] = v
        return v

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            if not self._replace(key):
                raise e
            return self._replacement(self, key)

    def __getattr__(self, key):
        if is_internal(key):
            return getattr(super(), key)
        return self.__getitem__(key)


class EphemeralAttrDict(MissingAttrDict):
    _replacement = EphemeralChain
