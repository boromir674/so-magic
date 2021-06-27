import pytest


@pytest.fixture
def test_infra():
    from so_magic.data.backend.backend import MyDecorator
    def func_logic(x):
        return x + 1
    def wrapper_logic(x):
        return x * 2

    class TestDecorator(MyDecorator):
        @classmethod
        def wrapper(cls, func, *args, **kwargs):
            result = func(*args, **kwargs)
            return wrapper_logic(result)

    def wrapper(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return wrapper_logic(result)

    return type('T', (object,), {
        'decorator': MyDecorator,
        'func_logic': func_logic,
        'wrapper_logic': wrapper_logic,
        'decorators': type('O', (object,), {
            'from_class': TestDecorator,
            'from_class_with_default_wrapper': type('TestDecorator', (MyDecorator,), {}),
            'from_dynamic_class': type('TestDecorator', (MyDecorator,), {'wrapper': wrapper}),
        })
    })


@pytest.mark.parametrize('usage_type, test_value, expected_value', [
    ('from_class', 1, 4),
    ('from_dynamic_class', 2, 6),
    ('from_class_with_default_wrapper', 2, 3),
])
def test_decorating_without_parenthesis(usage_type, test_value, expected_value, test_infra):
    magic_decorator = getattr(test_infra.decorators, usage_type).magic_decorator
    @magic_decorator
    def f1(x):
        return test_infra.func_logic(x)

    @magic_decorator()
    def f2(x):
        return test_infra.func_logic(x)

    assert f1(test_value) == f2(test_value) == expected_value
