import inspect
import types
import attr

from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator
from .client_code import PDTabularRetrieverDelegate, PDTabularIteratorDelegate, PDTabularMutatorDelegate


__all__ = ['PDTabularRetriever', 'PDTabularIterator', 'PDTabularMutator']


# INFRASTRUCTURE

def with_self(function):
    def _function(_self, *args, **kwargs):
        return function(*args, **kwargs)
    return _function


class Delegate:
    def __new__(cls, *args, **kwargs):
        delegate_ins = super().__new__(cls)
        tabular_operator = args[0]
        for _member_name, member in inspect.getmembers(
                tabular_operator, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])):
            if isinstance(member, types.FunctionType):  # if no decorator is used
                setattr(delegate_ins, member.__name__, types.MethodType(member, delegate_ins))
            if isinstance(member, types.MethodType):  # if @classmethod is used
                setattr(delegate_ins, member.__name__, types.MethodType(with_self(member), delegate_ins))
        return delegate_ins


tabular_operators = {
    'retriever': {
        'implementations': {
            'pd': PDTabularRetrieverDelegate,
        },
        'class_registry': EngineTabularRetriever,
    },
    'iterator': {
        'implementations': {
            'pd': PDTabularIteratorDelegate,
        },
        'class_registry': EngineTabularIterator,
    },
    'mutator': {
        'implementations': {
            'pd': PDTabularMutatorDelegate,
        },
        'class_registry': EngineTabularMutator,
    }
}


def get_operator(backend_id: str, operator_type: str):
    class_registry = tabular_operators[operator_type]['class_registry']
    
    @attr.s
    @class_registry.register_as_subclass(backend_id)
    class OperatorClass(class_registry):
        _delegate = attr.ib(
            default=attr.Factory(lambda: Delegate(tabular_operators[operator_type]['implementations'][backend_id])))

        def __getattr__(self, name: str):
            return getattr(self._delegate, name)

    return OperatorClass


# CONCRETE IMPLEMENTATIONS

PDTabularRetriever = get_operator('pd', 'retriever')
PDTabularIterator = get_operator('pd', 'iterator')
PDTabularMutator = get_operator('pd', 'mutator')
