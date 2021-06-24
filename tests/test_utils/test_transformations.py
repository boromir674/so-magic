import pytest


@pytest.fixture
def test_transformers():
    from so_magic.utils import Transformer
    def func1(a, b=2):
        return a * b + 1
    def func2(a, b, *, c=1):
        return a * b + c
    def func3(a, b, **kwargs):
        return a * b + kwargs.get('c', 1)
    return {
        'lambda': {
            'transformer': Transformer(lambda x: x + 1),
            'expected_nb_positional_args': 1,
            'kwarg_allowed': lambda key_to_check: False,
        },
        'func1': {
            'transformer': Transformer(func1),
            'expected_nb_positional_args': 1,
            'kwarg_allowed': lambda key_to_check: key_to_check in set(['b']),
        },
        'func2': {
            'transformer': Transformer(func2),
            'expected_nb_positional_args': 2,
            'kwarg_allowed': lambda key_to_check: key_to_check in set(['c']),
        },
        'func3': {
            'transformer': Transformer(func3),
            'expected_nb_positional_args': 2,
            'kwarg_allowed': lambda key_to_check: True,
        },
    }


@pytest.mark.parametrize('transformer, args_list, kwargs_dict, expected_result', [
    ('lambda', [1], {}, 2),
    ('lambda', [0], {}, 1),
    ('func1', [10], {}, 21),
    ('func1', [10], {'b': 3}, 31),
    # ('func2', [10, 2], {}, 21),  # this should work commented out
    # ('func2', [10, 2], {'c': 3}, 23),  # this should work commented out
    # ('func3', [10, 2], {}, 21),  # this should work commented out!
    # ('func3', [10, 2], {'a': 100}, 21),  # this should work commented out!
    # ('func3', [10, 2], {'c': 1}, 21),  # this should work commented out!
    # ('func3', [10, 2], {'c': 3}, 23),  # this should work commented out!
])
def test_transform_method(transformer, args_list, kwargs_dict, expected_result, test_transformers):
    assert expected_result == test_transformers[transformer]['transformer'].transform(*args_list, **kwargs_dict)


@pytest.fixture(params=[
    ['instance', ValueError, lambda x: f"Expected a callable as argument; instead got '{type(x)}'"],
    ['function', ValueError, lambda x: f"Expected a callable that receives at least one positional argument; instead got a callable that receives '{x.__code__.co_argcount}' arguments."],
])
def false_arguments(request):
    a = object()
    def f(): pass
    callables = {'instance': a, 'function': f}
    first_argument = callables[request.param[0]]
    return {'args': [first_argument],
            'exception': request.param[1],
            'exception_text': request.param[2](first_argument),
            }


def test_false_arguments(false_arguments):
    from so_magic.utils import Transformer
    with pytest.raises(false_arguments['exception'], match=false_arguments['exception_text']):
        _ = Transformer(*false_arguments['args'])


@pytest.fixture
def exception_message(test_transformers):
    def more_args_error(args_list, kwargs_dict, data):
        return rf"transform\(\) takes {data['expected_nb_positional_args'] + 1} positional arguments but {len(args_list) + 1} were given"
    
    def more_kwargs_error(args_list, kwargs_dict, data):
        unexpected_keywords = set([k for k in kwargs_dict.keys() if not data['kwarg_allowed'](k)])
        return rf"func1\(\) got an unexpected keyword argument '[{''.join(unexpected_keywords)}]'"
    
    e = {
        'more_args_error': more_args_error,
        'more_kwargs_error': more_kwargs_error,
    }
    def get_exception_message(transformer_id, args_list, kwargs_dict, error_type: str):   
        return e[error_type](args_list, kwargs_dict, test_transformers[transformer_id])
    return get_exception_message


@pytest.mark.parametrize('transformer_id, args_list, kwargs_dict, error_type', [
    ('lambda', [0, 2], {}, 'more_args_error'),
    ('func1', [2], {'b': 2, 'f': 8}, 'more_kwargs_error'),
    ('func1', [10, 20], {'b': 2}, 'more_args_error'),
    ('func1', [10, 3], {}, 'more_args_error'),
])
def test_wrong_transform_arguments(transformer_id, args_list, kwargs_dict, error_type, test_transformers, exception_message):
    transformer = test_transformers[transformer_id]['transformer']
    with pytest.raises(TypeError, match=exception_message(transformer_id, args_list, kwargs_dict, error_type)):
        _ = transformer.transform(*args_list, **kwargs_dict)
