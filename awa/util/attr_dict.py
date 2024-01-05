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
