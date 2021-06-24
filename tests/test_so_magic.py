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
def objects_to_test():
    def get_objects_to_test(so_master):
        return {
            'dtps_fct': so_master._data_manager.engine.backend.datapoints_factory,
            'cmd_fct': so_master._data_manager.engine.backend.command_factory,
            'phi_class': so_master._data_manager.phi_class,
            'rest': (
                so_master,
                so_master._data_manager,
                so_master._data_manager.engine,
                so_master._data_manager.engine.backend,
                so_master._data_manager.engine.datapoints_manager,
                so_master._data_manager.engine.backend.datapoints_factory.subject,
                so_master._data_manager.engine.backend.datapoints_factory.subject._observers,
                so_master._data_manager.phi_class.subject,
                so_master._data_manager.phi_class.subject._observers,
            )
        }
    return get_objects_to_test


@pytest.fixture(params=[[2]])
def so_magic_instances(request, objects_to_test):
    from so_magic import init_so_magic
    return [(i, objects_to_test(i)) for i in iter([init_so_magic() for _ in range(request.param[0])])]


def test_somagic_objects(so_magic_instances, assert_different_objects):
    from functools import reduce
    assert_different_objects(reduce(lambda i, j: i + j,
                                    ([x[1]['dtps_fct'], x[1]['cmd_fct'], x[1]['phi_class']] + list(x[1]['rest'])
                                     for x in so_magic_instances)))
    assert so_magic_instances[0][1]['phi_class'] != so_magic_instances[1][1]['phi_class']


def test_subscriptions(so_magic_instances):
    s = so_magic_instances[0]
    nb_observers = (1, 1, 1)

    assert s[1]['dtps_fct'].subject._observers[0] == s[0]._data_manager.engine.datapoints_manager
    assert s[1]['cmd_fct'].subject._observers[0] == s[0]._data_manager.commands_manager.command.accumulator
    assert s[1]['phi_class'].subject._observers[0] == s[0]._data_manager.built_phis
    assert all([len(subject._observers) == obs for subject, obs in zip(
        (s[1]['dtps_fct'].subject, s[1]['cmd_fct'].subject, s[1]['phi_class'].subject), nb_observers)])
