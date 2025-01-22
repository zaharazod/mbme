# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


def is_internal(key):
    return isinstance(key, str) and key.isidentifier() and key.startswith("__")


class AttrDict(dict):

    @property
    def _dict_class(self):
        return type(self)

    def __getitem__(self, key):
        if is_internal(key):
            return getattr(self, key)
        val = super().__getitem__(key)
        if type(key) is dict:
            new, changed = self._convert(val)
            if changed:
                self[key] = new
        return super().__getitem__(key)

    # def __getitem__(self, key):
    #     try:
    #         if is_internal(key):
    #             value = getattr(self, key)
    #         else:
    #             value = super().__getitem__(key)
    #             if isinstance(value, dict):
    #                 value, changed = self._convert(value)
    #                 if changed:
    #                     self[key] = value
    #     except Exception as e:
    #         raise e
    #     return value

    def __setitem__(self, key, value):
        if is_internal(key):
            return super().__setitem__(key, value)

        if type(key) is dict:
            new, changed = self._convert(value)
            if changed:
                value = new
        return super().__setitem__(key, value)

    # def __setitem__(self, key, value):
    #     if is_internal(key):
    #         return setattr(super(), key, value)
    #     value, _ = self._convert(value)
    #     super().__setitem__(key, value)
    #     return value

    def __getattr__(self, key):
        return getattr(super(), key) if is_internal(key) else self.__getitem__(key)

    def __setattr__(self, key, value):
        return (
            super().__setattr__(key, value)
            if is_internal(key)
            else self.__setitem__(key, value)
        )

    # def _convert(self, val):
    #     try:
    #         kls = (
    #             val.get('_dict_class', None)
    #             if callable(getattr(val, 'get', None))
    #             else None
    #         ) or self._dict_class
    #         return (
    #             (kls(val), True)
    #             if isinstance(val, dict) and type(val) is not kls
    #             else (
    #                 (list([v for v, _ in map(self._convert, val)]), True)
    #                 if isinstance(val, list)
    #                 else (val, False)
    #             )
    #         )
    #     except Exception as e:
    #         print(val)
    #         raise (e)

    def _convert(self, val):
        try:
            if not isinstance(val, dict):
                return (val, False)
            kls = (
                val.get("_dict_class", None)
                if callable(getattr(val, "get", None))
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

    # def _walk_self(self):
    #     for k,v in self.items():
    #         if type()
    n = []

    def _walk(self, node):
        try:
            print(f"walk: {node}")
            if isinstance(node, dict):
                items = node.items()
                for k, v in items:
                    if is_internal(k):
                        continue
                    n, c = self._check(v)
                    if c:
                        node[k] = n
                    self._walk(node[k])
            elif isinstance(node, (list, tuple)):
                for k, v in enumerate(node):
                    n, c = self._check(v)
                    if c:
                        node[k] = n

        except:
            print("OOPS")
            import sys

            sys.exit()

    def _check(self, val):
        if not isinstance(val, dict):
            return (val, False)
        print(f"check {val}")
        if type(val) is dict:
            new = self._dict_class(val)
            print(f"changed to {type(new)}")
            return (new, True)
        return (val, False)

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, AttrDict):
                v = v.to_dict()
            d[k] = v
        return d

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
