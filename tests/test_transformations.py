import pytest


@pytest.fixture
def transformers():
    from so_magic.utils import Transformer
    def gg(a, b=2):
        return a * b + 1
    return {'lambda': Transformer(lambda x: x + 1), 'gg': Transformer(gg)}


@pytest.mark.parametrize('transformer, args_list, kwargs_dict, expected_result', [
    ('lambda', [1], {}, 2),
    ('lambda', [0], {}, 1),
    pytest.param('lambda', [0, 2], {}, 1, marks=pytest.mark.xfail(raises=TypeError, reason="The lambda accepts a single argument and not two; transform() takes 2 positional arguments but 3 were given")),
    ('gg', [10], {}, 21),
    ('gg', [10], {'b': 3}, 31),
    pytest.param('gg', [2], {'b': 2, 'f':8}, 5, marks=pytest.mark.xfail(raises=TypeError, reason="The 'gg' function only allows the 'b' keyword argument and not the 'f'.")),
    pytest.param('gg', [10, 20], {'b': 2}, 31, marks=pytest.mark.xfail()),
])

def test_transform_method(transformer, args_list, kwargs_dict, expected_result, transformers):
    assert expected_result == transformers[transformer].transform(*args_list, **kwargs_dict)


@pytest.fixture(params=[
    ['instance', ValueError, lambda x: f"Expected a callable as argument; instead got '{type(x)}'"],
    ['function', ValueError, lambda x: f"Expected a callable that receives at least one positional argument; instead got a callable that receives '{x.__code__.co_argcount}'"],
])
def false_arguments(request):
    a = object()
    def f():
        pass
    callables = {'instance': a, 'function': f}
    first_argument = callables[request.param[0]]
    return {'args': [first_argument],
            'exception': request.param[1],
            'exception_text': request.param[2](first_argument),
            }


def test_false_arguments(false_arguments):
    from so_magic.utils import Transformer
    with pytest.raises(false_arguments['exception']) as e:
        _ = Transformer(*false_arguments['args'])
        assert false_arguments['exception_text'] == str(e)
