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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()})'

    def __getitem__(self, key):
        print('AttrDict', 'gi', key)
        
        try:
            if is_a(key, str) and key in self.__dict__:
                value = getattr(self, key)
                return value
            value = super().__getitem__(key)
            value, changed = type(self)._convert(value)
            if changed:
                self[key] = value
        except Exception as e:
            raise e
        return value

    def __setitem__(self, key, value):
        print('AttrDict', 'si', key, value)
        
        if is_internal(key):
            return super().__setattr__(key, value)
        
        value, _ = type(self)._convert(value)
        super().__setitem__(key, value)
        return value

    def __getattr__(self, key):
        print('AttrDict', 'ga', key)
        
        return self.__getitem__(key)

    def __setattr__(self, key, value): 
        print('AttrDict', 'sa', key, value)
        
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
        print('DottedAttrDict', 'gi', key)
        
        if is_dotted(key):
            parts = key.split('.')
            return self.__getitem__(parts.pop(0))['.'.join(parts)]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('DottedAttrDict', 'si', key, value)
        
        if is_internal(key):
            return super().__setitem__(key, value)
        if is_dotted(key):
            parts = key.split('.')
            key = parts.pop(0)
            new_path = '.'.join(parts)
            self[key] = type(self)()
            return super(type(self[key]), self[key]).__setitem__(new_path, value)
        return super().__setitem__(key, value)


class MissingAttrDict(AttrDict):
    def _replace(self, key):
        return is_a(key, str) and key.isalpha()

    def __getitem__(self, key):
        print('MissingAttrDict', 'gi', key)
        
        try:
            v = super().__getitem__(key)
            if not v:
                raise TypeError(f'missing {key}')
        except Exception as e:
            print('missing', key, e)
            if not self._replace(key):
                raise e
            v = type(self)()
            self.__dict__[key] = v
        print('MissingAttrDict', 'gi', key, v)
        return v

    def __getattr__(self, key):
        print('MissingAttrDict', 'ga', key)
        
        if is_internal(key):
            return getattr(super(), key)
        return self.__getitem__(key)
