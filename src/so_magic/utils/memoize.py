"""
Implementation of the object pool
"""
import attr

__all__ = ['ObjectsPool']


@attr.s
class ObjectsPool:
    """Class of objects that are able to return a reference to an object upon request.

    Whenever an object is requested, it is checked whether it exists in the pool.
    Then if it exists, a reference is returned, otherwise a new object is
    constructed (given the provided callable) and its reference is returned.

    Arguments:
        constructor (callable): able to construct the object given arguments
        objects (dict): the data structure representing the object pool
    """
    constructor = attr.ib(init=True)
    _objects = attr.ib(init=True, default={})

    def get_object(self, *args, **kwargs):
        r"""Request an object from the pool.

        Get or create an object given the input parameters. Existence in the pool is done using the
        python-build-in hash function. The input \*args and \*\*kwargs serve as
        input in the hash function to create unique keys with which to "query" the object pool.

        Returns:
            object: the reference to the object that corresponds to the input
            arguments, regardless of whether it was found in the pool or not
        """
        key = self._build_hash(*args, **kwargs)
        if key not in self._objects:
            self._objects[key] = self.constructor(*args, **kwargs)
        return self._objects[key]

    def _build_hash(self, *args, **kwargs):
        r"""Construct a unique string out of the input \*args and \*\*kwargs."""
        return hash('-'.join([str(_) for _ in args] + ['{key}={value}'.format(key=k, value=str(v)) for k, v in kwargs]))
