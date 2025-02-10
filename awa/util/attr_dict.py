# from collections import UserList

# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


def is_internal(key):
    return isinstance(key, str) and key.isidentifier() and key.startswith("_")


class AttrList(list):
    def __init__(self, iterator_arg=None, dict_class=None):
        self._dict_class = dict_class or AttrDict
        if iterator_arg:
            self.extend(iterator_arg)

    def insert(self, i, v):
        return super(AttrList, self).insert(i, self._dict_class._check(v))

    def append(self, v):
        return super(AttrList, self).append(self._dict_class._check(v))

    def extend(self, t):
        return super(AttrList, self).extend([self._dict_class._check(v) for v in t])

    def to_primitive(self):
        d = []
        for i in range(0, len(self)):
            if hasattr(i, "to_primitive"):
                i = i.to_primitive()
            d.append(list(i))
        return d

    to_list = to_primitive

    def __add__(self, t):
        return super(AttrList, self).__add__([self._dict_class._check(v) for v in t])

    def __iadd__(self, t):
        return super(AttrList, self).__iadd__([self._dict_class._check(v) for v in t])

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            return super(AttrList, self).__setitem__(
                i, [self._dict_class._check(v1) for v1 in v]
            )
        else:
            return super(AttrList, self).__setitem__(i, self._dict_class._check(v))

    def __setslice__(self, i, j, t):
        return super(AttrList, self).__setslice__(
            i, j, [self._dict_class._check(v) for v in t]
        )


class AttrDictCreator(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        if not hasattr(x, "_dict_class"):
            x._dict_class = x
        return x


class AttrDict(dict, metaclass=AttrDictCreator):
    _list_class = AttrList

    def __getitem__(self, key):
        if is_internal(key):
            return getattr(self, key)
        val = super().__getitem__(key)
        self[key] = self._check(val)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        return (
            super().__setitem__(key, value)
            if is_internal(key)
            else super().__setitem__(key, self._check(value))
        )

    def __getattr__(self, key):
        return getattr(super(), key) if is_internal(key) else self.__getitem__(key)

    def __setattr__(self, key, value):
        return (
            super().__setattr__(key, value)
            if is_internal(key)
            else self.__setitem__(key, value)
        )

    # def hasattr(self, attr):
    #     return hasattr(super(), attr)

    @classmethod
    def _walk(kls, node):
        if isinstance(node, dict):
            items = node.items()
        elif isinstance(node, (list, tuple)):
            items = enumerate(node)
        else:
            return node
        for k, v in items:
            if is_internal(k):
                continue
            node[k] = kls._check(v)
            kls._walk(node[k])
        return node

    @classmethod
    def _check(kls, val):
        if type(val) is dict:
            val, _ = kls._dict_class(val), True
        elif type(val) is list:
            val, _ = kls._list_class(val), True
        return val

    def to_primitive(self):
        d = {}
        for k, v in self.items():
            if hasattr(v, "to_primitive"):
                v = v.to_primitive()
            d[k] = v
        return d

    to_dict = to_primitive

    def merge(self, other, overwrite=True):
        kls = self._dict_class or type(self)
        for k, v in other.items():
            if all(map(lambda v: isinstance(v, dict), [self.get(k, None), v])):
                z = [kls(self[k]), kls(v)]
                if not overwrite:
                    z.reverse()
                z[0].merge(z[1], overwrite)
                self[k] = z[0]
            elif overwrite or k not in self:
                self[k] = v
            else:
                pass  # no overwrite existing
        self._walk(self)


# TODO: support for nested assignment -> recursive _dict_class creation
class FalseChain(object):

    __getitem__ = __getattr__ = lambda s, *a, **k: s

    # def __str__(s): return ''
    def __bool__(s):
        return False


FALSE = FalseChain()
DUMMY_VALUE = -23.005


class MissingAttrDict(AttrDict):
    def __init__(self, *args, default_value=FALSE, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_value = default_value

    def _replace(self, key):
        return isinstance(key, str) and key.isidentifier() and not is_internal(key)

    def setdefault(self, k, dv):
        if k not in self or self[k] is FALSE:
            self[k] = dv

    def get(self, key, default=DUMMY_VALUE):  # FIXME should use **kwargs
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
            return (
                self._default_value(key)
                if callable(self._default_value)
                else self._default_value
            )
