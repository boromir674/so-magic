import pytest


@pytest.fixture
def data_engine_type():
    """Our EngineType metaclass that helps devs define different data engines (ie pandas).

    Returns:
        type: the EngineType metaclass
    """
    from so_magic.data.backend.backend import BackendType
    assert type(BackendType) == type
    return BackendType


@pytest.fixture
def data_engine_class(data_engine_type):
    """Our DataEngine class that helps devs create different data engines (ie pandas).

    Returns:
        EngineType: the DataEngine class
    """
    from so_magic.data.backend.backend import EngineBackend
    assert type(EngineBackend) == data_engine_type
    return EngineBackend


@pytest.fixture
def engine_attributes():
    """The important attributes that each data engine (eg pandas engine) is expected to have upon creation."""
    return (
        'registry',
        '_commands',
        # 'command',
    )


@pytest.fixture
def engine_creation_assertions(engine_attributes, data_engine_class, data_engine_type):
    """Execute the necessary assertion statements related to testing the creation of a new Data Engine."""
    def make_assertions(engine_object, engine_name: str):
        """Assert that the creation and initialization of a new engine was as expected.

        Args:
            engine_object (so_magic.data.backend.engine.EngineType): [description]
            engine_name (str): the engine name to reference it
        """
        assert engine_object == getattr(data_engine_class, engine_name)
        assert engine_name in data_engine_class.subclasses
        assert type(getattr(data_engine_class, engine_name)) == data_engine_type
        assert all(hasattr(getattr(data_engine_class, engine_name), x) for x in engine_attributes)
        assert len(getattr(data_engine_class, engine_name).registry) == 0
    return make_assertions


@pytest.mark.parametrize('engine_specs', [
    # Scenario 1 -> create 2 engines, with the below names
    (['engine1',
      'engine2']),
])
def test_engine_registration(engine_specs, engine_creation_assertions, engine_attributes, data_engine_class):
    """Test that new engines have their attributes correctly initialized"""
    for engine_data in engine_specs:
        data_engine = data_engine_class.new(engine_data)
        engine_creation_assertions(data_engine, engine_data)

    expected_distinct_ids = len(engine_specs) + 1

    for engine_attribute in engine_attributes:
        assert len(set([id(getattr(getattr(data_engine_class, engine_name), engine_attribute)) for engine_name in engine_specs] + [id(data_engine_class.registry)])) == expected_distinct_ids
