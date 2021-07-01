import pytest


@pytest.fixture
def test_datapoints_full_file_path():
    import os
    return lambda file_name: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'dts', file_name)


@pytest.fixture
def sample_json(test_datapoints_full_file_path):
    return test_datapoints_full_file_path('sample-data.jsonlines')

@pytest.fixture
def sample_collaped_json(test_datapoints_full_file_path):
    return test_datapoints_full_file_path('sample-data-collapsed.jsonlines')


@pytest.fixture
def datapoint_files_to_test(sample_collaped_json, sample_json):
    import pandas as pd
    import numpy as np
    return {
        'data_1': {
            'data_path': sample_collaped_json,
            'nb_rows': 100,
            'nb_columns': 46,
            'type_distros': {
                'type': {str: 100},
                'flavors': {list: 98, type(None): 2},
            },
            'value_distros': {
                'type': {'hybrid': 48, 'sativa': 19, 'indica': 33},
            },
            'row': {
                0: {
                    'flavors': [lambda v: v == ["Chemical", "Pine", "Diesel"],
                                lambda v: type(v) == list,
                                ],
                    'type': [lambda v: v == 'hybrid',
                             lambda v: type(v) == str,
                             ],
                },
                7: {
                    'flavors': [lambda v: v == ["Earthy", "Pungent", "Sweet"],
                                lambda v: type(v) == list,
                                ],
                    'type': [lambda v: v == 'hybrid',
                             lambda v: type(v) == str,
                             ],
                },
                76: {
                    'flavors': [lambda v: v is None,
                                lambda v: pd.isnull(v),
                                lambda v: isinstance(v, type(None)),
                                ],
                },
                87: {
                    'flavors': [lambda v: v is None,
                                lambda v: type(v) == type(None),
                                ],
                },
            },
            'column_names': (
                'flavors',
                'name',
                'description',
                'image_urls',
                'parents',
                '_id',
                'type',
                'image_paths',
                'Aroused',
                'Creative',
                'Energetic',
                'Euphoric',
                'Focused',
                'Giggly',
                'Happy',
                'Hungry',
                'Relaxed',
                'Sleepy',
                'Talkative',
                'Tingly',
                'Uplifted',
                'Cramps',
                'Depression',
                'Eye Pressure',
                'Fatigue',
                'Headaches',
                'Inflammation',
                'Insomnia',
                'Lack of Appetite',
                'Muscle Spasms',
                'Nausea',
                'Pain',
                'Seizures',
                'Spasticity',
                'Stress',
                'Anxious',
                'Dizzy',
                'Dry Eyes',
                'Dry Mouth',
                'Headache',
                'Paranoid',
                'difficulty',
                'flowering',
                'height',
                'stretch',
                'yield',
            ),
        },
        'data_2': {
            'data_path': sample_json,
            'nb_rows': 100,
            'nb_columns': 12,
            'type_distros': {
                'type': {str: 100},
                'flavors': {list: 98, float: 2},
            },
            'value_distros': {
                'type': {'hybrid': 48, 'sativa': 19, 'indica': 33},
            },
            'row': {
                0: {
                    'flavors': [lambda v: v == ["Chemical", "Pine", "Diesel"],
                                lambda v: type(v) == list,
                                ],
                    'type': [lambda v: v == 'hybrid',
                             lambda v: type(v) == str
                             ],
                },
                7: {
                    'flavors': [lambda v: v == ["Earthy", "Pungent", "Sweet"],
                                lambda v: type(v) == list,
                                ],
                    'type': [lambda v: v == 'hybrid',
                             lambda v: type(v) == str
                             ],
                },
                76: {
                    'flavors': [lambda v: np.isnan(v),
                                lambda v: pd.isnull(v),
                                lambda v: type(v) == float,
                                ],
                },
                87: {
                    'flavors': [lambda v: np.isnan(v),
                                lambda v: pd.isnull(v),
                                lambda v: type(v) == float,
                                ],
                },
            },
            'column_names': (
                'flavors',
                'name',
                'medical',
                'description',
                'image_urls',
                'parents',
                'negatives',
                'grow_info',
                '_id',
                'type',
                'image_paths',
                'effects',
            ),
        },
    }
