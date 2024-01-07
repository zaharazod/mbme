import sys
from typing import Any
from logging import getLogger, INFO, StreamHandler

logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(StreamHandler(sys.stdout))
log = logger.info

# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

is_internal = lambda key: isinstance(key, str) and key.startswith('__')
is_dotted = lambda key: isinstance(key, str) and '.' in key

class AttrDict:
    
    def __init__(self, *args, **kwargs):
        self.__data__ = dict(*args, **kwargs)

    def __str__(self):
        return self.__data__.__str__()

    def __getitem__(self, key):
        try:
            value = self.__data__[key]
            if type(value) is dict:
                log('get: converting to attr')
                value = AttrDict(value)
                self[key] = value
        except Exception as e:
            raise e
        return value
    
    def __setitem__(self, key, value):
        dict_class = type(self)
        if is_internal(key):
            return super().__setattr__(key, value)        
        if type(value) is dict:
            value = dict_class(value)
        self.__data__[key] = value
        return value
    
    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __getattr__(self, key):
        if hasattr(self.__data__, key):
            value = getattr(self.__data__, key)
            return value
        return self.__getitem__(key)


class DottedAttrDict(AttrDict):
    
    def __getitem__(self, key):
        if is_dotted(key):
            parts = key.split('.')
            return self.__getitem__(parts.pop(0))['.'.join(parts)]
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        dict_class = type(self)
        if is_internal(key):
            return super().__setitem__(key, value)
        if is_dotted(key):
            parts = key.split('.')
            key = parts.pop(0)
            new_path = '.'.join(parts)
            self[key] = dict_class()
            return super(type(self[key]), self[key]).__setitem__(new_path, value)
        return super().__setitem__(key, value)
