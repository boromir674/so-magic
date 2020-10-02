from abc import abstractmethod, ABC
from functools import wraps
import inspect
from so_magic.utils import Singleton, Transformer, ObjectRegistry, Subject


class PhiFunctionRegistry(Singleton, ObjectRegistry):
    def __new__(cls, *args, **kwargs):
        x = Singleton.__new__(cls, *args, **kwargs)
        x = ObjectRegistry(getattr(x, 'objects', {}))
        return x

    @staticmethod
    def get_instance():
        return PhiFunctionRegistry()

    @staticmethod
    def get_name(a_callable):
        if hasattr(a_callable, 'name'):
            return a_callable.name
        if hasattr(a_callable, '__code__') and hasattr(a_callable.__code__, 'co_name'):
            return a_callable.__code__.co_name
        if hasattr(type(a_callable), 'name'):
            return type(a_callable).name
        if hasattr(type(a_callable), '__name__'):
            return type(a_callable).__name__
        return ''


phi_registry = PhiFunctionRegistry()


class PhiFunctionMetaclass(type):
    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        x.subject = Subject([])
        return x


class PhiFunctionRegistrator(metaclass=PhiFunctionMetaclass):

    @classmethod
    def register(cls, phi_name=''):
        def wrapper(a_callable):
            if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
                print(f"Registering input function {a_callable.__code__.co_name}")
                cls._register(a_callable, key_name=phi_name)
            else:
                if not hasattr(a_callable, '__call__'):
                    raise RuntimeError(f"Expected an class definition with a '__call__' instance method defined 1. Got {type(a_callable)}")
                members = inspect.getmembers(a_callable)
                if not ('__call__', a_callable.__call__) in members:
                    raise RuntimeError(f"Expected an class definition with a '__call__' instance method defined 2. Got {type(a_callable)}")
                print(f"Registering a class {type(a_callable).__name__}")
                instance = a_callable()
                cls._register(instance, key_name=phi_name)
            return a_callable
        return wrapper

    @classmethod
    def _register(cls, a_callable, key_name=None):
        key = key_name if key_name else PhiFunctionRegistry.get_name(a_callable)
        print(f"Registering object {a_callable} at key {key}.")
        phi_registry.add(key, a_callable)
        cls.subject.name = key
        cls.subject.state = a_callable
        cls.subject.notify()

    @classmethod
    def my_decorator(cls, f):
        print(f"Running 'my_decorator' with input type {type(f)}")
        @wraps(f)
        def wrapper(*args, **kwds):
            if hasattr(f, '__code__'):  # it a function (def func_name ..)
                print(f"Registering input function {a_callable.__code__.co_name}")
                cls._register(f)
            else:
                if not hasattr(f, '__call__'):
                    raise RuntimeError(f"Expected an class definition with a '__call__' instance method defined 1. Got {type(f)}")
                members = inspect.getmembers(f)
                if not ('__call__', f.__call__) in members:
                    raise RuntimeError(f"Expected an class definition with a '__call__' instance method defined 2. Got {type(f)}")
                print(f"Registering a class {type(a_callable).name}")
                instance = f()
                cls._register(instance)
            return f(*args, **kwds)
        return wrapper


if __name__ == '__main__':
    reg1 = PhiFunctionRegistry()
    reg2 = PhiFunctionRegistry()
    reg3 = PhiFunctionRegistry.get_instance()

    assert id(reg1) == id(reg2) == id(reg3)

    @PhiFunctionRegistrator.my_decorator
    def example():
        """Inherited Docstring"""
        print('Called example function')


    example()

    print(example.__name__)
    print('--')
    print(example.__doc__)
