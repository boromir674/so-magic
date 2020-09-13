from abc import ABC

__all__ = ['ObjectRegistry', 'ObjectRegistryError']


class ObjectRegistry(ABC):
    """Simple dict-like retrieval/inserting "store" facility."""

    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls)
        if args:
            x.objects = args[0]
        else:
            x.objects = {}
        return x

    def add(self, key, value):
        if self.objects.get(key, None):
            raise ObjectRegistryError(f"Requested to insert value {value} in already existing key {key}."
                                      f"All keys are [{', '.join(_ for _ in self.objects)}]")
        self.objects[key] = value

    def remove(self, key):
        if key not in self.objects:
            raise ObjectRegistryError(f"Requested to remove item with key {key}, which does not exist.")
        self.objects.pop(key)

    def pop(self, key):
        if key not in self.objects:
            raise ObjectRegistryError(f"Requested to remove item with key {key}, which does not exist.")
        return self.objects.pop(key)

    def get(self, key):
        if key not in self.objects:
            raise ObjectRegistryError(f"Requested to get item with key {key}, which does not exist.")
        return self.objects[key]

    def __contains__(self, item):
        return item in self.objects

class ObjectRegistryError(Exception): pass
