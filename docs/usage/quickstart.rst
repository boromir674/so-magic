***************
Quickstart
***************

| The most common case is to infer a self-organising map given some data.
| Assuming you have a file with data in JSON-lines format, then you could "train" a model uising the following code:

.. code-block:: python

    # Please re-configure
    my_json_lines_file_path = 'path-to-json-lines-data'


    from so_magic import init_so_magic
    somagic = init_so_magic()

    somagic.load_data(my_json_lines_file_path, id='test_data')
    ATTRS = ['hybrid', 'indica', 'sativa']
    ATTRS2 = ['type_hybrid', 'type_indica', 'type_sativa']
    from functools import reduce
    UNIQUE_FLAVORS = reduce(lambda i, j: set(i).union(set(j)),
                            [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if _ is not None])

    if not getattr(somagic.dataset, 'feature_vectors', None):
        cmd = somagic._data_manager.command.select_variables
        cmd.args = [[{'variable': 'type', 'columns': ATTRS2}, {'variable': 'flavors', 'columns': list(UNIQUE_FLAVORS)}]]
        cmd.execute()

        cmd = somagic._data_manager.command.one_hot_encoding
        cmd.args = [somagic._data_manager.datapoints, 'type']
        cmd.execute()

        # cmd2
        cmd = somagic._data_manager.command.one_hot_encoding_list
        cmd.args = [somagic._data_manager.datapoints, 'flavors']
        cmd.execute()

    import numpy as np
    setattr(somagic.dataset, 'feature_vectors', np.array(somagic._data_manager.datapoints.observations[ATTRS2 + list(UNIQUE_FLAVORS)]))
    # somagic.dataset.feature_vectors = np.array(somagic._data_manager.datapoints.observations[ATTRS2 + list(UNIQUE_FLAVORS)])

    print("ID", id(somagic.dataset))

    som = somagic.map.train(*train_args[:2], maptype=train_args[2], gridtype=train_args[3])



.. _SO: https://stackoverflow.com/

.. _somoclu documentation: https://somoclu.readthedocs.io/en/stable/

.. _installation methods: https://somoclu.readthedocs.io/en/stable/download.html
