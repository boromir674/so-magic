import pytest


def test_datapoint(og_kush):
    assert og_kush.name == 'Og Kush'
    assert hasattr(og_kush, 'images')

