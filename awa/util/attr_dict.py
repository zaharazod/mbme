# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


def is_internal(key): return isinstance(key, str) and key.startswith('__')
def is_dotted(key): return isinstance(key, str) and '.' in key
def is_a(o, t): return issubclass(type(o), t)
def is_dict(o): return is_a(o, (dict, AttrDict))

class AttrDict(object):

    def __init__(self, *args, **kwargs):
        self.__data__ = dict(*args, **kwargs)

    def __str__(self):
        return str(self.__data__)

    def __repr__(self):
        return f'{type(self).__name__}({repr(self.__data__)})'

    def __getitem__(self, key):
        try:
            if is_a(key, str) and hasattr(self.__data__, key):
                value = getattr(self.__data__, key)
                return value
        except Exception as e:
            raise(e)
        try:
            value = self.__data__[key]
            if type(value) is dict:
                value = type(self)(value)
                self[key] = value
        except Exception as e:
            raise e
        return value

    def __setitem__(self, key, value):
        if is_internal(key):
            return super().__setattr__(key, value)
        if type(value) is dict:
            value = type(self)(value)
        self.__data__[key] = value
        return value

    __getattr__ = __getitem__
    __setattr__ = __setitem__

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class FalseChain:

    __call__ = __getitem__ = __getattr__ = lambda self, *a, **k: self
    def __bool__(self): return False


FALSE = FalseChain()

class MissingAttrDict(AttrDict):
    
    def __getitem__(self, key):
        try:
            return super().get(key)
        except Exception:
            return FALSE

    __getattr__ = __getitem__
