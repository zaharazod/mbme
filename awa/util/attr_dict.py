from typing import Any
# cf. -- may reimplement but this interface works
# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattr__(self, __key: Any) -> Any:
        return self.__getitem__(__key)
        
    def __getitem__(self, __key: Any) -> Any:
        value = super().__getitem__(__key)
        if isinstance(value, dict):
            self[__key] = value = AttrDict(value)
        return value

    def __setitem__(self, __key: Any, value: Any) -> Any:
        if isinstance(value, dict):
            value = AttrDict(value)
        return super().__setitem__(__key, value)
    
    def __setattr__(self, __key: Any, value: Any) -> Any:
        if isinstance(__key, str) and __key.startswith('__'):
            return super().__setattr__(__key, value)
        return self.__setitem__(__key, value)
        
