import pytest


@pytest.mark.parametrize('train_args', [
    ([6, 8, 'toroid', 'hexagonal']),
    # ([12, 12, 'toroid', 'rectangular'])
])
def test_somagic_scenario(train_args, somagic, test_dataset, sample_collaped_json):
    attrs = ('width', 'height', 'type', 'grid_type')
    som = somagic.map.train(*train_args[:2], maptype=train_args[2], gridtype=train_args[3])
    assert som.dataset_name == sample_collaped_json
    assert all(parameter == getattr(som, attribute) for attribute, parameter in zip(attrs, train_args))


@pytest.fixture
def so_magic_instances():
    from so_magic import init_so_magic
    return [init_so_magic(), init_so_magic()]


@pytest.mark.parametrize('nb_objects, nb_observers', [
    (2, [(1, 1, 1),
         (1, 1, 1)]),
])
def test_somagic_objects(nb_objects, so_magic_instances, nb_observers):
    assert id(so_magic_instances[0]) != id(so_magic_instances[1])
    assert id(so_magic_instances[0]._data_manager) != id(so_magic_instances[1]._data_manager)
    assert id(so_magic_instances[0]._data_manager.engine) != id(so_magic_instances[1]._data_manager.engine)
    assert id(so_magic_instances[0]._data_manager.engine.backend) != id(so_magic_instances[1]._data_manager.engine.backend)
    assert id(so_magic_instances[0]._data_manager.engine.datapoints_manager) != id(so_magic_instances[1]._data_manager.engine.datapoints_manager)

    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory)
    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory.subject) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory.subject)
    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory.subject._observers) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory.subject._observers)

    assert id(so_magic_instances[0]._data_manager.engine.backend.command_factory) != id(so_magic_instances[1]._data_manager.engine.backend.command_factory)

    assert so_magic_instances[0]._data_manager.phi_class != so_magic_instances[1]._data_manager.phi_class
    assert id(so_magic_instances[0]._data_manager.phi_class) != id(so_magic_instances[1]._data_manager.phi_class)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject) != id(so_magic_instances[1]._data_manager.phi_class.subject)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject._observers) != id(so_magic_instances[1]._data_manager.phi_class.subject._observers)


def test_subscriptions(so_magic_instances):
    s = so_magic_instances[0]
    datapoints_fact = s._data_manager.engine.backend.datapoints_factory
    cmd_fact = s._data_manager.engine.backend.command_factory
    phi_class = s._data_manager.phi_class
    nb_observers = (1, 1, 1)
    subjects = [datapoints_fact.subject,
                cmd_fact.subject,
                phi_class.subject
                ]

    assert datapoints_fact.subject._observers[0] == s._data_manager.engine.datapoints_manager
    assert cmd_fact.subject._observers[0] == s._data_manager.commands_manager.command.accumulator
    assert phi_class.subject._observers[0] == s._data_manager.built_phis
    assert all([len(subject._observers) == column for subject, column in zip(subjects, nb_observers)])
