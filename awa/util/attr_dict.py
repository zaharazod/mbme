# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
from pprint import pp


def is_internal(key): return isinstance(key, str) and key.startswith('_')
def is_dotted(key): return isinstance(key, str) and '.' in key


class AttrDict(dict):

    @classmethod
    def _convert(cls, val):
        return (cls(val), True) \
            if isinstance(val, dict) \
            and type(val) is not cls \
            else (val, False)

    def to_dict(self):
        d = dict(self)
        for k, v in d.items():
            if isinstance(v, AttrDict):
                d[k] = v.to_dict()
        return d

    def __repr__(self):
        # return f'{type(self).__name__}({super().__repr__()})'
        return super().__repr__()

    def __getitem__(self, key):
        try:
            if isinstance(key, str) and key in self.__dict__:
                value = super().__getitem__(key)
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

    def merge(self, other):
        for k, v in other.items():
            if all(map(lambda v: isinstance(v, dict), [self.get(k, None), v])):
                z = type(self)(self[k])
                z.merge(v)
                self[k] = z
            else:
                self[k] = v

    # def update(self, other=None):
    #     # pp({
    #     #     'WHAT': 'UPDATE',
    #     #     'who': self,
    #     #     'other': other
    #     # })
    #     if not other:
    #         # print('updating nothing??', other, self)
    #         return
    #     for k, v in other.items():
    #         if all(map(lambda v: isinstance(v, dict), [self.get(k, None), v])):
    #             # if isinstance(v, dict) and isinstance(self.get(k, None), dict):
    #             # pp({
    #             #     'what': 'recursive update',
    #             #     'self': self,
    #             #     'key': k,
    #             #     'ours': self[k],
    #             #     'theirs': v
    #             # })
    #             print('merge', k, v)
    #             self[k].merge(v)
    #             # pp({
    #             #     'what': 'updated recursive',
    #             #     'self': self,
    #             #     'key': k,
    #             #     'new': self[k]
    #             # })
    #         else:
    #             v, _ = type(self)._convert(v)
    #             # pp({
    #             #     'what': 'regular assign',
    #             #     'self': self,
    #             #     'k': k, 'v': v})
    #             self[k] = v


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
        return isinstance(key, str) \
            and re.match(r'^[a-zA-Z_]+$', key)

    def setdefault(self, k, dv):
        if not self[k]:
            self[k] = dv

    def get(self, key, default=DUMMY_VALUE):
        try:
            v = super().__getitem__(key)
            return v
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

    def __getattr__(self, key):
        return getattr(super(), key) \
            if is_internal(key) \
            else self.__getitem__(key)
