import pytest


@pytest.mark.parametrize('train_args', [
    ([10, 10, 'toroid', 'hexagonal']),
    # ([12, 12, 'toroid', 'rectangular'])
])
def test_somagic_scenario(train_args, somagic, sample_collaped_json):
    somagic.load_data(sample_collaped_json, id='test_data')
    if not getattr(somagic.dataset, 'feature_vectors', None):
        cmd = somagic._data_manager.command.select_variables
        cmd.args = [['type', 'flavours']]
        cmd.execute()
        #
        # cmd = somagic._data_manager.command.encode_nominal_scalar
        # cmd.args = ['type']
        # cmd.execute()

        # cmd = somagic._dataset_manager.command.select_variables
        # cmd.args = ['type', 'flavours']
        # cmd.execute()
    # som = somagic.map.train(*train_args[:2])
    #
    # attrs = ('height', 'width', 'type', 'grid_type')
    #
    # assert all(hasattr(som.som, x) for x in attrs)


@pytest.mark.parametrize('nb_objects, nb_observers', [
    (2, [(1, 1, 1),
         (1, 1, 1)]),
])
def test_somagic_objects(nb_objects, nb_observers):
    from green_magic import init_so_magic
    so_magic_instances = [init_so_magic() for _ in range(nb_objects)]

    assert id(so_magic_instances[0]._data_manager.backend) != id(so_magic_instances[1]._data_manager.backend)
    assert id(so_magic_instances[0]._data_manager.backend.engine) != id(so_magic_instances[1]._data_manager.backend.engine)
    assert id(so_magic_instances[0]._data_manager.backend.datapoints_manager) != id(so_magic_instances[1]._data_manager.backend.datapoints_manager)

    assert id(so_magic_instances[0]._data_manager.backend.datapoints_factory) != id(so_magic_instances[1]._data_manager.backend.datapoints_factory)
    assert id(so_magic_instances[0]._data_manager.backend.datapoints_factory.subject) != id(so_magic_instances[1]._data_manager.backend.datapoints_factory.subject)
    assert id(so_magic_instances[0]._data_manager.backend.datapoints_factory.subject._observers) != id(so_magic_instances[1]._data_manager.backend.datapoints_factory.subject._observers)

    assert id(so_magic_instances[0]._data_manager.backend.engine.command_factory) != id(so_magic_instances[1]._data_manager.backend.engine.command_factory)

    assert so_magic_instances[0]._data_manager.phi_class != so_magic_instances[1]._data_manager.phi_class
    assert id(so_magic_instances[0]._data_manager.phi_class) != id(so_magic_instances[1]._data_manager.phi_class)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject) != id(so_magic_instances[1]._data_manager.phi_class.subject)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject._observers) != id(so_magic_instances[1]._data_manager.phi_class.subject._observers)

    for i, s in enumerate(so_magic_instances):
        datapoints_fact = s._data_manager.backend.datapoints_factory
        cmd_fact = s._data_manager.backend.engine.command_factory
        phi_class = s._data_manager.phi_class

        subjects = [datapoints_fact.subject,
                    cmd_fact,
                    phi_class.subject
                    ]
        assert len(set([id(x._observers) for x in subjects])) == len(subjects)

        assert datapoints_fact.subject._observers[0] == s._data_manager.backend.datapoints_manager
        assert cmd_fact._observers[0] == s._data_manager.commands_manager.command.accumulator
        assert phi_class.subject._observers[0] == s._data_manager.built_phis
        assert all([len(subject._observers) == column for subject, column in zip(subjects, nb_observers[i])])
