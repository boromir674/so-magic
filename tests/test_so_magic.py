import pytest


@pytest.mark.parametrize('train_args', [
    ([6, 8, 'toroid', 'hexagonal']),
    # ([12, 12, 'toroid', 'rectangular'])
])
def test_somagic_scenario(train_args, somagic, sample_collaped_json):
    somagic.load_data(sample_collaped_json, id='test_data')
    ATTRS = ['hybrid', 'indica', 'sativa']
    ATTRS2 = ['type_hybrid', 'type_indica', 'type_sativa']
    from functools import reduce
    UNIQUE_FLAVORS = reduce(lambda i, j: set(i).union(set(j)),
                            [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if _ is not None])

    if not getattr(somagic.dataset, 'feature_vectors', None):
        cmd = somagic._data_manager.command.select_variables
        cmd.args = [[{'variable': 'type', 'columns': ATTRS2}, {'variable': 'flavors', 'columns': list(UNIQUE_FLAVORS)}]]
        cmd.execute()

        assert set([x['variable'] for x in somagic._data_manager.feature_manager.feature_configuration.variables]) == {'type', 'flavors'}

        assert all(type(x) == str for x in somagic._data_manager.datapoints.observations['type'])
        assert set(ATTRS) == set([_ for _ in somagic._data_manager.datapoints.observations['type']])

        import pandas as pd
        assert set(ATTRS) == set(pd.unique(somagic._data_manager.datapoints.observations['type']))

        cmd = somagic._data_manager.command.one_hot_encoding
        cmd.args = [somagic._data_manager.datapoints, 'type']
        cmd.execute()

        assert all(x in somagic._data_manager.datapoints.observations.columns for x in ATTRS2)
        assert all(sum([datarow[_] for _ in ATTRS2]) == 1 and len([datarow[_] for _ in ATTRS2 if datarow[_] == 1]) == 1 for index, datarow in somagic._data_manager.datapoints.observations[ATTRS2].iterrows())

        # cmd2
        assert set([type(x) for x in somagic._data_manager.datapoints.observations['flavors']]) == {list, type(None)}

        # assert all([type(x) == list for x in somagic._data_manager.datapoints.observations['flavors']])

        # set([]) pd.unique(somagic._data_manager.datapoints.observations['flavors'])
        MAX_FLAVORS_PER_DAATPOINT = max([len(x) for x in [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if type(_) is list]])
        MIN = 0
        assert len(UNIQUE_FLAVORS) > 5
        nb_columns_before = len(somagic._data_manager.datapoints.observations.columns)

        cmd = somagic._data_manager.command.one_hot_encoding_list
        cmd.args = [somagic._data_manager.datapoints, 'flavors']
        cmd.execute()

        assert nb_columns_before + len(UNIQUE_FLAVORS) == len(somagic._data_manager.datapoints.observations.columns)

        assert all(x in somagic._data_manager.datapoints.observations.columns for x in UNIQUE_FLAVORS)
        assert all(0 <= sum([datarow[_] for _ in UNIQUE_FLAVORS]) <= MAX_FLAVORS_PER_DAATPOINT for index, datarow in somagic._data_manager.datapoints.observations[list(UNIQUE_FLAVORS)].iterrows())

    import numpy as np
    setattr(somagic.dataset, 'feature_vectors', np.array(somagic._data_manager.datapoints.observations[ATTRS2 + list(UNIQUE_FLAVORS)]))
    # somagic.dataset.feature_vectors = np.array(somagic._data_manager.datapoints.observations[ATTRS2 + list(UNIQUE_FLAVORS)])

    assert hasattr(somagic.dataset, 'feature_vectors')

    print("ID", id(somagic.dataset))

    attrs = ('width', 'height', 'type', 'grid_type')

    som = somagic.map.train(*train_args[:2], maptype=train_args[2], gridtype=train_args[3])
    assert som.dataset_name == sample_collaped_json
    assert all(parameter == getattr(som, attribute) for attribute, parameter in zip(attrs, train_args))


@pytest.mark.parametrize('nb_objects, nb_observers', [
    (2, [(1, 1, 1),
         (1, 1, 1)]),
])
def test_somagic_objects(nb_objects, nb_observers):
    from so_magic import init_so_magic
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
