import abc
import inspect
import types
from functools import wraps

__all__ = ['Transformer']

class TransformerInterface(abc.ABC):
    """The interface defining a method to transform structured data. Anyone, implementing this has the ability to receive
    some kind of data and return some kind of transformed version of them.
    """
    @abc.abstractmethod
    def transform(self, data, **kwargs):
        """Takes data and optional keyword arguments and transforms them.
        Input data can represent either a single variable of an observation (scalar)
        or a vector of observations of the same variable (if N observations then returns a [N x 1] array-like).

        Example 1:
        obs1 = [x1, y1, z1]
        fa = f_a(x)
        fb = f_b(x)
        fc = f_c(x)
        feature_vector1 = [fa(x1), fb(y1), fc(z1)]

        So, each of fa, fb and fc can implement the Transformer interface.

        Example 2:
        obs1 = [x1, y1, z1]
        obs2 = [x2, y2, z2]
        obs3 = [x3, y3, z3]
        obs4 = [x4, y4, z4]
        data = [obs1;
                obs2;
                obs3;
                obs4]  shape = (4,3)
        fa = f_a(x)
        fb = f_b(x)
        fc = f_c(x)
        feature_vectors = [fa(data[:0], fb(data[:1], fc(data[:2])]  - shape = (4,3)

        Again each of fa, fb and fc can implement the Transformer interface.

        Args:
            data (object): the input data to transform; the x in an f(x) invocation

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError


class RuntimeTransformer(TransformerInterface, abc.ABC):
    """Examines whether the input object is callable, if it can receive at least one input argument and also
    whether it can accept kwargs. Depending on the kwargs check, "configures" the '_transform' method to process
     any kwargs at runtime or to ignore them.

    Delegates all the transformation operation to its '_transform' method provided by its '_callable' field.

    Args:
        a_callable (callable): a callable object used to delegate the transformation operation
    """
    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls)
        a_callable = args[0]
        if not callable(a_callable):
            raise ValueError(f"Expected a callable as argument; instead got '{type(a_callable)}'")
        nb_mandatory_arguments = a_callable.__code__.co_argcount  # this counts sums both *args and **kwargs
        # use syntax like 'def a(b, *, c=1, d=2): .. to separate pos args from kwargs and to inform 'inspect' lib about it
        if nb_mandatory_arguments < 1:
            raise ValueError(f"Expected a callable that receives at least one positional argument; instead got a callable that "
                             f"receives '{nb_mandatory_arguments}'")
        signature = inspect.signature(a_callable)
        parameters = [param for param in signature.parameters.values()]

        if 1 < nb_mandatory_arguments:
            def _transform(self, data, **keyword_args):
                return a_callable(data, **keyword_args)
            x._transform = types.MethodType(_transform, x)
        elif nb_mandatory_arguments == len(parameters):
            def _transform(self, data, **keyword_args):
                return a_callable(data)
            x._transform = types.MethodType(_transform, x)
        else:
            raise Exception(f"Something went really bad. Check code above. Parameters: [{', '.join(str(_) for _ in parameters)}]")
        x._callable = a_callable
        return x

    def transform(self, data, **kwargs):
        return self._transform(data, **kwargs)

class Transformer(RuntimeTransformer): pass