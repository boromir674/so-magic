import inspect
import types
import attr

from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator
from .client_code import PDTabularRetrieverDelegate, PDTabularIteratorDelegate, PDTabularMutatorDelegate


__all__ = ['PDTabularRetriever', 'PDTabularIterator', 'PDTabularMutator']


# INFRASTRUCTURE

def with_self(function):
    # foo_code = compile(f'def {f_name}({arg_string}): return f({params_str})', "<string>", "exec")
    # foo_func1 = types.FunctionType(foo_code.co_consts[0], globals(), f_name)

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


def validate_delegate(tabular_operator, required_members):
    for member_name, required_signature in required_members:
        sig = str(inspect.signature(getattr(tabular_operator, member_name)))
        if sig != required_signature:
            raise ValueError(f"Expected signature {required_signature} for {member_name} member of object "
                             f"{tabular_operator} with type {type(tabular_operator)}. Instead got {sig}.")


RETRIEVER_REQUIRED_SIGNATURES = {
        'column': '(identifier, data)',
        'row': '(identifier, data)',
        'nb_columns': '(data)',
        'nb_rows': '(data)',
        'get_numerical_attributes': '(data)',
    }


# CONCRETE IMPLEMENTATIONS

@attr.s
@EngineTabularRetriever.register_as_subclass('pd')
class PDTabularRetriever(EngineTabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""
    _delegate = attr.ib(default=attr.Factory(lambda: Delegate(PDTabularRetrieverDelegate)),
                        # validator=lambda x, y, z: validate_delegate(z, RETRIEVER_REQUIRED_SIGNATURES)
                        )

    def column(self, identifier, data):
        return self._delegate.column(identifier, data)

    def row(self, identifier, data):
        return self._delegate.row(identifier, data)

    def nb_columns(self, data):
        return self._delegate.nb_columns(data)

    def nb_rows(self, data):
        return self._delegate.nb_rows(data)

    def get_numerical_attributes(self, data):
        return self._delegate.get_numerical_attributes(data)


@attr.s
@EngineTabularIterator.register_as_subclass('pd')
class PDTabularIterator(EngineTabularIterator):
    """The observation object is the same as the one your return from 'from_json_lines'"""
    _delegate = attr.ib(default=attr.Factory(lambda: Delegate(PDTabularIteratorDelegate)))

    def columnnames(self, data):
        return self._delegate.columnnames(data)

    def iterrows(self, data):
        return self._delegate.iterrows(data)

    def itercolumns(self, data):
        return self._delegate.itercolumns(data)


@attr.s
@EngineTabularMutator.register_as_subclass('pd')
class PDTabularMutator(EngineTabularMutator):
    _delegate = attr.ib(default=attr.Factory(lambda: Delegate(PDTabularMutatorDelegate)))

    def add_column(self, datapoints, values, new_attribute, **kwargs):
        self._delegate.add_column(datapoints, values, new_attribute, **kwargs)
