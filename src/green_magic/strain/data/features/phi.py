from abc import abstractmethod,ABC
import types
import attr


class PhiFunctionInterface(ABC):
    """Each datapoint"""
    @abstractmethod
    def __call__(self, data, **kwargs):
        raise NotImplementedError


class AbstractPhiFunction(PhiFunctionInterface):
    @abstractmethod
    def __call__(self, data, **kwargs):
        raise NotImplementedError


@attr.s
class PhiFunction(AbstractPhiFunction):
    function = attr.ib(init=True)

    @function.validator
    def is_function(self, attribute, input_value):
        if not callable(input_value):
            raise ValueError(f"Expected a callable object; instead a {type(input_value)} was given.")
        if input_value.func_code.co_argcount != 1:
            raise ValueError(
                f"Expected a callable that takes exactly 1 positional argument and optional keyword-arguments; instead a callable that takes {input_value.func_code.co_argcount} arguments was given.")

    def __call__(self, data, **kwargs):
        return self.function(data, **kwargs)

    @classmethod
    def register(cls, a_callable):
        if type(data) == types.FunctionType:
            pass


class PhiFunctionFactory:
    pass

class PhiFunctionManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.functions = {}
        return cls._instance

    def register(self, function):
       pass


