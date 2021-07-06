from abc import ABC, abstractmethod
from typing import Dict
import inspect
import attr
import pandas as pd
from so_magic.utils import SubclassRegistry


class DiscretizerInterface(ABC):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


class AbstractDiscretizer(DiscretizerInterface):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


@attr.s
class BaseDiscretizer(AbstractDiscretizer):
    binner = attr.ib()

    def discretize(self, *args, **kwargs):
        """Expects args: dataset, feature and kwargs; 'nb_bins'."""
        datapoints = args[0]
        attribute = args[1]
        bins = args[2]
        try:
            output = self.binner.bin(datapoints.column(attribute), bins, **kwargs)
        except TypeError as type_error:
            msg = f'Table column being processed: {attribute}. Exception text: {str(type_error)}'
            raise TypeError(msg) from type_error

        return output


@attr.s
class FeatureDiscretizer(BaseDiscretizer):
    feature = attr.ib(init=True)

    def discretize(self, *args, **kwargs):
        """Expects args: dataset, nb_bins."""
        return super().discretize(args[0], self.feature, args[1])

@attr.s
class FeatureDiscretizerFactory:
    binner_factory = attr.ib(init=True)

    def categorical(self, feature, **kwargs) -> FeatureDiscretizer:
        binner_type = 'same-length'
        if kwargs.get('quantisized', False):
            binner_type = 'quantisized'
        return FeatureDiscretizer(self.binner_factory.create_binner(binner_type), feature)

    def numerical(self, feature, **kwargs) -> FeatureDiscretizer:
        binner_type = 'same-length'
        if kwargs.get('quantisized', False):
            binner_type = 'quantisized'
        return FeatureDiscretizer(self.binner_factory.create_binner(binner_type), feature)


#########################################

class BinnerInterface(ABC):
    @abstractmethod
    def bin(self, values, bins):
        raise NotImplementedError


@attr.s
class BaseBinner(BinnerInterface):
    algorithm = attr.ib()

    def bin(self, values, bins):
        """It is assumed numerical (ratio or interval) variable or ordinal (not nominal) categorical variable."""
        try:
            return self.algorithm.run(values, bins)
        except TypeError as type_error:
            raise TypeError(f'Exception text: {str(type_error)}. Possible reasons: preprocessing is needed to make sure'
                            f' suitable values are places in missing entries and/or all entries are of the same type') \
                from type_error


class BinnerClass(metaclass=SubclassRegistry): pass


class BinnerFactory:
    parent_class = BinnerClass

    def equal_length_binner(self, *args, **kwargs) -> BaseBinner:
        """Binner that create bins of equal size (max_value - min_value)"""
        raise NotImplementedError

    def quantisized_binner(self, *args, **kwargs) -> BaseBinner:
        """Binner that will adjust the bin sizes so that the observations are evenly distributed in the bins

        Raises:
            NotImplementedError: [description]

        Returns:
            BaseBinner: [description]
        """
        raise NotImplementedError

    def create_binner(self, *args, **kwargs) -> BaseBinner:
        raise NotImplementedError


class AlgorithmInterface(ABC):
    """The Algorithm interface provides implementing classes with the 'run' method that executes some business logic.

    Inherit from this interface if you want to use the 'Strategy Pattern' in your classes.
    """
    @abstractmethod
    def run(self, *args, **kwargs):
        """Run the algorithm, given any arguments and keyword arguments.

        Executes the strategy/logic.
        """
        raise NotImplementedError


@attr.s
class AlgorithmArguments:
    """An algorithm's expected positional arguments.
    
    Instances of this class represent the (positional) arguments that an algorithm requires as input
    to operate.

    Take the example of a sorting algorithm. A sorting algorithm operates on an array (or list),
    so one might add a list to an AlgorithmArguments' instance.
    On the other hand whether the algorithm sorts in descending or ascending order could be an optional algorithm parameter
    and thus not be included in the AlgorithmArguments' instance.

    Args:
        arg_types (tuple): zero or more types of the required arguments by an algorithm to operate
        default_values (tuple): zero or more values to use as default, for the right-most arguments that the client did not supply at runtime
    Returns:
        Iterable: the rows of the (data) table
    """
    arg_types: tuple = attr.ib()
    default_values: tuple = attr.ib()
    _required_args = attr.ib(init=False, default=attr.Factory(lambda self: len(self.arg_types), takes_self=True))

    def values(self, *args):
        """Get list of arguments, given the provided values.

        In case of missing arguments, the default values are added.

        Raises:
            AlgorithmArgumentsError: [description]

        Returns:
            list: the list of argument values
        """
        if len(args) > len(self._required_args):
            raise AlgorithmArgumentsError(f'Given more than the supported number of arguments. '
                                          f'{len(args)} > {len(self._required_args)}')
        if len(args) + len(self.default_values) < len(self._required_args):
            raise AlgorithmArgumentsError(f'Given insufficient number of arguments. '
                                          f'given={len(args)}, default={len(self.default_values)}, required={self._required_args}')
        missing = len(self._required_args) - len(args)
        computed_args_list = list(args) + self.default_values[-missing:]
        if not all(isinstance(arg_value, self.arg_types[i]) for i, arg_value in computed_args_list):
            raise AlgorithmArgumentsError('Type missmatch')
        return computed_args_list


@attr.s
class AbstractAlgorithm(AlgorithmInterface, ABC):
    """Uses a callback, arguments and optional parameters to run the algorithm.

    Args:
        callback (callable): the algorithm's business logic
        arguments (list): the algorithm's required arguments to operate on
        parameters (dict): the algorithm's optional parameters
    """
    callback: callable = attr.ib()
    arguments: list = attr.ib(default=attr.Factory(list))
    parameters: Dict[str, object] = attr.ib(default=attr.Factory(dict))
    default_parameter_values = attr.ib(init=False, default=attr.Factory(
        lambda self: {k: v['value'] for k, v in self.parameters.items()}, takes_self=True))
    _args = attr.ib(init=False, default=attr.Factory(list))


@attr.s
class MagicAlgorithm(AbstractAlgorithm):
    """Algorithm that stores its output in the 'output' property."""
    _signature = attr.ib(init=False,
                         default=attr.Factory(lambda self: inspect.signature(self.callback), takes_self=True))
    _output = attr.ib(init=False, default=attr.Factory(dict))

    def run(self, *args, **kwargs):
        """Run the algorithm, using the given (required) arguments and optional parameters.

        Use the args to pass required arguments and the kwargs to pass optional parameters.

        Raises:
            MagicAlgorithmError: [description]
            MagicAlgorithmError: [description]

        Returns:
            [type]: [description]
        """
        if not len(args) == len(self.arguments):
            raise MagicAlgorithmError(
                f'Number of runtime positional arguments do not match the expected number of positional argumnets. '
                f'Given {len(args)} arguments: [{", ".join(str(_) for _ in args)}]. Expected {len(self.arguments)} '
                f'arguments: [{", ".join(str(_) for _ in self.arguments)}].')
        if not all(isinstance(argument, self.arguments[i]) for i, argument in enumerate(args)):
            raise MagicAlgorithmError(f'Bad positional argument for algorithm. Expected arguments with types '
                                      f'[{", ".join(self.arguments)}]. Instead got [{", ".join(self.arguments)}].')
        self._args = list(args)
        self.update_parameters(**kwargs)
        result = self._run_callback()
        self._output['settings'] = self._get_settings(result)
        self._output['result'] = self._get_result(result)
        return self._output

    def _run_callback(self):
        return self.callback(*self._args, **{k: v['value'] for k, v in self.parameters.items()})

    @property
    def output(self):
        return self._output

    def _get_result(self, result):
        return result

    def _get_settings(self, _result):
        return {
            'arguments': self._args,
            'parameters': {
                param_name: param_data['value'] for param_name, param_data in self.parameters.items()
            },
        }

    def update_parameters(self, **kwargs):
        if not all(isinstance(parameter_value, self.parameters['type']) for parameter_name, parameter_value in kwargs
                   if parameter_name in self.parameters):
            raise MagicAlgorithmParametersError(
                f'Bad algorithm parameters. Allowed parameters with types '
                f'[{", ".join(f"{k}: {v}" for k, v in self.parameters.items())}]. '
                f'Instead got [{", ".join(f"{k}: {v}" for k, v in kwargs.items())}].')
        self._update_params(**kwargs)

    def set_default_parameters(self):
        self._update_params(**self.default_parameter_values)

    def _update_params(self, **kwargs):
        for key, value in kwargs.items():
            self.parameters[key]['value'] = value


class MagicAlgorithmError(Exception): pass
class MagicAlgorithmParametersError(Exception): pass
class AlgorithmArgumentsError(Exception): pass


def call_method(a_callable):
    def _call(_self, *args, **kwargs):
        return a_callable(*args, **kwargs)
    return _call


@attr.s
class Discretizer(BaseDiscretizer):

    @property
    def algorithm(self):
        return self.binner.algorithm

    @classmethod
    def from_algorithm(cls, alg):
        binner = BaseBinner(alg)
        return Discretizer(binner)

# import typing

# PNT = typing.TypeVar('PNT', str)

# KT = typing.TypeVar('KT')
# VT = typing.Type[KT]

# class ParameterGeneric(typing.Generic[KT]):
#     def __getitem__(self, key: KT) -> typing.Type[KT]:
#         raise NotImplementedError


# class ParameterDataDict(typing.Generic[KT]):
#     def __getitem__(self, key: PNT) -> ParameterGeneric[KT]:
#         raise NotImplementedError


class BinningAlgorithm(metaclass=SubclassRegistry):

    @classmethod
    def from_built_in(cls, algorithm_id):
        return cls.create(algorithm_id,
                          pd.cut,
                          # TODO replace with call to dataclass
                          [object, object],
                          {
                              'right': {
                                  'type': bool,
                                  'value': True,
                              },
                              'labels': {
                                  'type': object,
                                  'value': None
                              },
                              'retbins': {
                                  'type': bool,
                                  'value': True
                              },
                              'precision': {
                                  'type': int,
                                  'value': 3
                              },
                              'include_lowest': {
                                  'type': bool,
                                  'value': False
                              },
                              'duplicates': {
                                  'type': str,
                                  'value': 'raise'
                              },
                          }
                          )


@BinningAlgorithm.register_as_subclass('pd.cut')
class PDCutBinningAlgorithm(MagicAlgorithm):

    def _get_settings(self, result):
        return dict(super()._get_settings(result), **{'used_bins': result[1]})

    def _get_result(self, result):
        if bool(self.parameters['retbins']):
            return super()._get_result(result)[0]
        return super()._get_result(result)
