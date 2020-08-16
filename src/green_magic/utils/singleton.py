from abc import ABC

__all__ = ['Singleton']


class Singleton(ABC):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

