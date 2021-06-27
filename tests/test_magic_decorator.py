import pytest


@pytest.fixture
def test_infra():
    from so_magic.data.backend.backend import MyDecorator
    class TestDecorator(MyDecorator):
        @classmethod
        def wrapper(cls, func, *args, **kwargs):
            result = func(*args, **kwargs)
            return result * 2

    def wrapper(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2

    test_decorator_class_1 = type('TestDecorator', (MyDecorator,), {})
    test_decorator_class_2 = type('TestDecorator', (MyDecorator,), {'wrapper': wrapper})

    return type('T', (object,), {
        'decorator': MyDecorator,
        'decorators': type('O', (object,), {
            'from_class': TestDecorator,
            'from_class_with_default_wrapper': test_decorator_class_1,
            'from_dynamic_class': test_decorator_class_2,
            '__iter__': lambda self: iter((TestDecorator, test_decorator_class_1, test_decorator_class_2))
        })()
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
        return x + 1

    @magic_decorator()
    def f2(x):
        return x + 1

    @magic_decorator(1)
    def f3(x):
        return x + 1

    assert f1(test_value) == f2(test_value) == f3(test_value) == expected_value


def test_inheriting_from_my_decorator(test_infra, assert_different_objects):
    assert_different_objects([x.magic_decorator for x in test_infra.decorators])
    assert_different_objects([x.wrapper for x in test_infra.decorators])
