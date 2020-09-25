import pytest
from so_magic.utils import MapOnLinearSpace
from so_magic.utils.linear_mapping import LinearScale


@pytest.mark.parametrize('lower_bound, upper_bound, wrong_index', [
    (20, 100, 2),
    pytest.param(20, 20, 2, marks=pytest.mark.xfail(raises=ValueError, reason="lower_bound < upper_bound should be true; The lower bound of a linear scale is restricted to be strictly smaller than the upper bound")),
    pytest.param(80, 20, 2, marks=pytest.mark.xfail(raises=ValueError, reason="lower_bound < upper_bound should be true; The lower bound of a linear scale is restricted to be strictly smaller than the upper bound")),
])
def test_linear_scale(lower_bound, upper_bound, wrong_index):
    scale = LinearScale(lower_bound, upper_bound)
    assert scale.lower_bound == lower_bound
    assert scale.upper_bound == upper_bound
    assert len(scale) == 2


@pytest.mark.parametrize('from_scale, target_scale, reverse, input_value, output_value', [
    ([0, 400], [0, 100], True, 50, 87.5),
    ([0, 400], [0, 100], True, 100, 75),
    ([0, 400], [0, 100], True, 25, 93.75),
    ([0, 400], [0, 100], True, 10, 97.5),
    ([0, 400], [0, 100], True, 400, 0),
    ([0, 400], [0, 100], True, 0, 100),
    ([0, 400], [0, 100], False, 50, 12.5),
    ([0, 400], [0, 100], False, 100, 25),
    ([0, 400], [0, 100], False, 25, 6.25),
    ([0, 400], [0, 100], False, 10, 2.5),
    ([0, 400], [0, 100], False, 400, 100),
    ([0, 400], [0, 100], False, 0, 0),
])
def test_linear_transformation(from_scale, target_scale, reverse, input_value, output_value):
    linear_transformer = MapOnLinearSpace.universal_constructor(from_scale, target_scale, reverse=reverse)
    assert all(hasattr(linear_transformer, x) for x in ('from_scale', 'target_scale', 'reverse'))
    assert hasattr(linear_transformer, 'from_scale')
    assert linear_transformer.transform(input_value) == output_value

    linear_transformer.reverse = not linear_transformer.reverse
    assert linear_transformer.transform(input_value) == target_scale[1] - output_value

    linear_transformer.reverse = False
    linear_transformer.from_scale = [0, 10]
    linear_transformer.target_scale = [0, 100]
    assert linear_transformer.transform(7) == 70
