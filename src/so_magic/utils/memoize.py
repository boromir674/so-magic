import attr

__all__ = ['ObjectsPool']


@attr.s
class ObjectsPool:
    """A generic object pool able to return a reference to an object upon request. Whenever an object is requested a
    hash is built out of the (request) arguments, which is then checked against the registry of keys to determine
    whether the object is present in the pool or to create (using the local constructor attribute) and insert a new one
     (in the pool)."""
    constructor = attr.ib(init=True)
    _objects = attr.ib(init=True, default={})

    def get_object(self, *args, **kwargs):
        key = self._build_hash(*args, **kwargs)
        if key not in self._objects:
            self._objects[key] = self.constructor(*args, **kwargs)
        return self._objects[key]

    def _build_hash(self, *args, **kwargs):
        """Construct a unique string out of the arguments that the constructor receives."""
        return hash('-'.join([str(_) for _ in args]))

    def __getattr__(self, item):
        return self._objects[item]
