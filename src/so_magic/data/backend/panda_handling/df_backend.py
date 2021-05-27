import inspect
import types
import attr
from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator

__all__ = ['PDTabularRetriever', 'PDTabularIterator', 'PDTabularMutator']


# DELEGATES
# User defined (engine dependent implementations of tabular operations)

class PDTabularRetrieverDelegate(EngineTabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    @classmethod
    def column(cls, identifier, data):
        return data.observations[identifier]

    @classmethod
    def row(cls, identifier, data):
        return data.observations.loc(identifier)

    @classmethod
    def nb_columns(cls, data):
        return len(data.observations.columns)

    @classmethod
    def nb_rows(cls, data):
        print('\n------ DEBUG NB ROWS PDTabularRetrieverDelegate DATA TYPE', type(data), ' ------\n')
        return len(data.observations)

    @classmethod
    def get_numerical_attributes(cls, data):
        return data.observations._get_numeric_data().columns.values


class PDTabularIteratorDelegate(EngineTabularIterator):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    @classmethod
    def columnnames(cls, data):
        return list(data.observations.columns)

    @classmethod
    def iterrows(cls, data):
        return iter(data.observations.iterrows())

    @classmethod
    def itercolumns(cls, data):
        return iter(data.observations[column] for column in data.observations.columns)


class PDTabularMutatorDelegate(EngineTabularMutator):

    @classmethod
    def add_column(cls, datapoints, values, new_attribute, **kwargs):
        datapoints.observations[new_attribute] = values


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
            print()
        return delegate_ins


def validate_retriever_delegate(_self, _attribute, value):
    members_list = list(inspect.getmembers(value,
                                           predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))
    assert all(x in (_[0] for _ in members_list) for x in ('row', 'column', 'nb_rows', 'nb_columns',
                                                            'get_numerical_attributes'))
    for member_name, _member in members_list:
        if member_name in ['row', 'column']:
            sig = str(inspect.signature(getattr(value, member_name)))
            if sig != '(identifier, data)':
                raise ValueError(f"Expected signature (identifier, data) for {member_name} of retriever {value}. "
                                 f"Instead got {sig}.")
        if member_name in ['nb_rows', 'nb_columns', 'get_numerical_attributes']:
            sig = str(inspect.signature(getattr(value, member_name)))
            if sig != '(data)':
                raise ValueError(f"Expected signature (data) for {member_name} of retriever {value}. "
                                 f"Instead got {sig}.")


# CONCRETE IMPLEMENTATIONS

@attr.s
@EngineTabularRetriever.register_as_subclass('pd')
class PDTabularRetriever(EngineTabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""
    _delegate = attr.ib(default=attr.Factory(lambda: Delegate(PDTabularRetrieverDelegate)),
    # validator=validate_retriever_delegate
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
