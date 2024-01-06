import sys
from typing import Any
from logging import getLogger, INFO, StreamHandler
logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(StreamHandler(sys.stdout))
log = logger.info

# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute


class AttrDict:
    def __init__(self, *args, **kwargs):
        log('attr.init')
        self.__data__ = dict(*args, **kwargs)

    def __getitem__(self, key):
        log(f'attr.getitem {key}')
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
        if type(value) is dict:
            log('set: converting')
            value = AttrDict(value)
        self.__data__[key] = value
        return value

    def __getattr__(self, key):
        log(f'attr.getattr {key}')
        if hasattr(self.__data__, key):
            return getattr(self.__data__, key)
        return self.__getitem__(key)

