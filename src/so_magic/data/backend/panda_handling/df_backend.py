import inspect
import types
import attr

from so_magic.data.magic_datapoints_factory import BroadcastingDatapointsFactory
from so_magic.data.interfaces import TabularRetriever, TabularIterator, TabularMutator
from so_magic.data.backend.backend import EngineBackend
from ..backend_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator, BackendSpecifications
from .client_code import BACKEND


# INFRASTRUCTURE

def with_self(function):
    def _function(_self, *args, **kwargs):
        return function(*args, **kwargs)
    return _function


class Delegate:
    def __init__(self, tabular_operator):
        for _member_name, member in inspect.getmembers(
                tabular_operator, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])):
            if isinstance(member, types.FunctionType):  # if no decorator is used
                setattr(self, member.__name__, types.MethodType(member, self))
            if isinstance(member, types.MethodType):  # if @classmethod is used
                setattr(self, member.__name__, types.MethodType(with_self(member), self))


tabular_operators = {
    'retriever': {
        'interface': TabularRetriever,
        'class_registry': EngineTabularRetriever,
    },
    'iterator': {
        'interface': TabularIterator,
        'class_registry': EngineTabularIterator,
    },
    'mutator': {
        'interface': TabularMutator,
        'class_registry': EngineTabularMutator,
    }
}

BUILT_IN_BACKENDS_DATA = [
    BACKEND,
]


@attr.s
class EngineBackends:
    backend_interfaces = attr.ib()
    _interface_2_name = attr.ib(init=False, default=attr.Factory(
        lambda self: {v['interface']: interface_id for interface_id, v in self.backend_interfaces.items()},
        takes_self=True))
    implementations = attr.ib(init=False, default=attr.Factory(dict))
    backends = attr.ib(init=False, default=attr.Factory(dict))
    # id of the backend that is currently being registered/built
    __id: str = attr.ib(init=False, default='')

    @staticmethod
    def from_initial_available(backends):
        engine_backends = EngineBackends(tabular_operators)
        engine_backends.add(*list(backends))
        return engine_backends

    @property
    def defined_interfaces(self):
        return self.backend_interfaces.keys()

    @property
    def defined_backend_names(self):
        return self.implementations.keys()

    def __iter__(self):
        return iter((backend_name, interfaces_dict) for backend_name, interfaces_dict in self.implementations.items())

    def _get_interface_names(self, backend_id):
        """Get the names of the interfaces that the backend has found to implement."""
        return self.implementations[backend_id].keys()

    def add(self, *backend_implementations):
        for backend_implementation in backend_implementations:
            self._add(backend_implementation)

    def _add(self, backend_implementation):
        self.__id = backend_implementation['backend_id']
        implemented_interfaces = backend_implementation['interfaces']
        self.implementations[self.__id] =\
            {self.name(implementation): implementation for implementation in implemented_interfaces}
        self.register(backend_implementation)

    def name(self, interface_implementation):
        return self._interface_2_name[inspect.getmro(interface_implementation)[1]]

    def register(self, backend_implementation: dict):
        for implemented_interface_name in self._get_interface_names(self.__id):
            self.define_operator(self.__id, implemented_interface_name)
        # Build
        backend_specs = BackendSpecifications(self.__id, backend_implementation['backend_name'])
        backend = EngineBackend.new(self.__id)
        # init backend attributes
        backend_specs(backend)
        backend.datapoints_factory = BroadcastingDatapointsFactory()
        self.backends[self.__id] = backend

    def define_operator(self, backend_id, operator_type: str):
        class_registry = self.backend_interfaces[operator_type]['class_registry']

        @attr.s
        @class_registry.register_as_subclass(backend_id)
        class _OperatorClass(class_registry):
            _delegate = attr.ib(
                default=attr.Factory(lambda: Delegate(self.implementations[backend_id][operator_type])))

            def __getattr__(self, name: str):
                return getattr(self._delegate, name)


def magic_backends():
    return EngineBackends.from_initial_available(BUILT_IN_BACKENDS_DATA)
