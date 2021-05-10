"""This module is responsible to provide a formal way of registering phi functions
at runtime. See the 'PhiFunctionRegistrator' class and its 'register' decorator method
"""
import logging
import inspect
from typing import Callable
from so_magic.utils import Singleton, ObjectRegistry, Subject

logger = logging.getLogger(__name__)


class PhiFunctionRegistry(Singleton, ObjectRegistry):
    """A Singleton dict-like object registry for phi functions.

    Use this class to create a singleton object (instance of this class) that
    acts as a storage for phi function objects.
    """
    def __new__(cls, *args, **kwargs):
        """Create a new (singleton) instance and initialize an empty registry.

        Returns:
            PhiFunctionRegistry: the reference to the singleton object (instance)
        """
        phi_function_registry = Singleton.__new__(cls, *args, **kwargs)
        phi_function_registry = ObjectRegistry(getattr(phi_function_registry, 'objects', {}))
        return phi_function_registry

    @staticmethod
    def get_instance():
        """Get the singleton object (instance).

        Returns:
            PhiFunctionRegistry: the reference to the singleton object (instance)
        """
        return PhiFunctionRegistry()


phi_registry = PhiFunctionRegistry()


class PhiFunctionMetaclass(type):
    """Class type with a single broadcasting (notifies listeners) facility.

    Classes using this class as metaclass, obtain a single broadcasting facility
    as a class attribute. The class attribute is called 'subject' can be referenced
    as any class attribute.

    Example:
        class MyExampleClass(metaclass=PhiFunctionMetaclass):
            pass

        instance_object_1 = MyExampleClass()
        instance_object_2 = MyExampleClass()
        assert id(MyExampleClass.subject) == id(instance_object_1.subject) == id(instance_object_2.subject)
    """
    def __new__(mcs, *args, **kwargs):
        """Create a new class type object and set the 'subject' attribute to a new Subject instance; the broadcaster.

        Returns:
            PhiFunctionMetaclass: the new class type object
        """
        phi_function_class = super().__new__(mcs, *args, **kwargs)
        phi_function_class.subject = Subject([])
        return phi_function_class


class PhiFunctionRegistrator(metaclass=PhiFunctionMetaclass):
    """Add phi functions to the registry and notify observers/listeners.

    This class provides the 'register' decorator, that client can use to decorate either functions (defined with the
    def python special word), or classes (defined with the python class special word).
    """

    # NICE TO HAVE: make the decorator work without parenthesis
    @classmethod
    def register(cls, phi_name=''):
        """Add a new phi function to phi function registry and notify listeners/observers.

        Use this decorator around either a callable function (defined with the 'def' python special word) or a class
        with a takes-no-arguments (or all-optional-arguments) constructor and a __call__ magic method.

        All phi functions are expected to be registered with a __name__ and a __doc__ attribute.

        You can select your custom phi_name under which to register the phi function or default to an automatic
        determination of the phi_name to use.

        Automatic determination of phi_name is done by examining either the __name__ attribute of the function or the
        class name of the class.

        Example:

            >>> from so_magic.data.features.phi import PhiFunctionRegistry, PhiFunctionRegistrator

            >>> registered_phis = PhiFunctionRegistry()

            >>> @PhiFunctionRegistrator.register()
            ... def f1(x):
            ...  return x * 2
            Registering input function f1 as phi function, at key f1.

            >>> input_value = 5
            >>> print(f"{input_value} * 2 = {registered_phis.get('f1')(input_value)}")
            5 * 2 = 10

            >>> @PhiFunctionRegistrator.register()
            ... class f2:
            ...  def __call__(self, data, **kwargs):
            ...   return data + 5
            Registering input class f2 instance as phi function, at key f2.

            >>> input_value = 1
            >>> print(f"{input_value} + 5 = {registered_phis.get('f2')(input_value)}")
            1 + 5 = 6

            >>> @PhiFunctionRegistrator.register('f3')
            ... class MyCustomClass:
            ...  def __call__(self, data, **kwargs):
            ...   return data + 1
            Registering input class MyCustomClass instance as phi function, at key f3.

            >>> input_value = 3
            >>> print(f"{input_value} + 1 = {registered_phis.get('f3')(input_value)}")
            3 + 1 = 4

        Args:
            phi_name (str, optional): custom name to register the phi function. Defaults to automatic computation.
        """
        def wrapper(a_callable):
            """Add a callable object to the phi function registry and preserve info for __name__ and __doc__ attributes.

            The callable object should either be function (defined with def) or a class (defined with class). In case of
            a class the class must have a constructor that takes no arguments (or all arguments are optional) and a
            __call__ magic method.

            Registers the callable as a phi function under the given or automatically computed name, makes sure the
            __name__ and __doc__ attributes preserve information and notifies potential listeners/observers.

            Args:
                a_callable (Callable): the object (function or class) to register as phi function
            """
            if hasattr(a_callable, '__code__'):  # it is a function (def func_name ..)
                logging.info("Registering input function %s as phi function.", a_callable.__code__.co_name)
                key = phi_name if phi_name else cls.get_name(a_callable)
                print(f"Registering input function {a_callable.__code__.co_name} as phi function, at key {key}.")
                cls._register(a_callable, key)
            else:
                if not hasattr(a_callable, '__call__'):
                    raise RuntimeError("Expected an class definition with a '__call__' instance method defined 1."
                                       f" Got {type(a_callable)}")
                members = inspect.getmembers(a_callable)
                if ('__call__', a_callable.__call__) not in members:
                    raise RuntimeError("Expected an class definition with a '__call__' instance method defined 2."
                                       f" Got {type(a_callable)}")
                instance = a_callable()
                instance.__name__ = a_callable.__name__
                instance.__doc__ = a_callable.__call__.__doc__
                key = phi_name if phi_name else cls.get_name(instance)
                print(f"Registering input class {a_callable.__name__} instance as phi function, at key {key}.")
                cls._register(instance, key)
            return a_callable
        return wrapper

    @classmethod
    def _register(cls, a_callable, key_name):
        """Register a callable as phi function and notify potential listeners/observers.

        The phi function is registered under the given key_name or in case of None the name is automatically computed
        based on the input callable.

        Args:
            a_callable (Callable): the callable that holds the business logic of the phi function
            key_name (str, optional): custom phi name. Defaults to None, which means automatic determination of the name
        """
        phi_registry.add(key_name, a_callable)
        cls.subject.name = key_name
        cls.subject.state = a_callable
        cls.subject.notify()

    @staticmethod
    def get_name(a_callable: Callable):
        """Get the 'name' of the input callable object

        Args:
            a_callable (Callable): a callable object to get its name

        Returns:
            str: the name of the callable object
        """
        if hasattr(a_callable, 'name'):
            return a_callable.name
        if hasattr(a_callable, '__code__') and hasattr(a_callable.__code__, 'co_name'):
            return a_callable.__code__.co_name
        if hasattr(type(a_callable), 'name'):
            return type(a_callable).name
        if hasattr(type(a_callable), '__name__'):
            return type(a_callable).__name__
        # TODO replace below line with a raise Exception
        # we want to cause an error when we fail to get a sensible string name
        return ''


if __name__ == '__main__':
    reg1 = PhiFunctionRegistry()
    reg2 = PhiFunctionRegistry()
    reg3 = PhiFunctionRegistry.get_instance()

    assert id(reg1) == id(reg2) == id(reg3)

    @PhiFunctionRegistrator.register
    def example():
        """Inherited Docstring"""
        print('Called example function')

    example()

    print(example.__name__)
    print('--')
    print(example.__doc__)

    reg1.get('example')()
