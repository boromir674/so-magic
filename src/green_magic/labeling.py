import sys
import inspect


def _create_labeler(labeler_type):
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if hasattr(obj, 'name') and labeler_type == obj.name:
                return obj()
    else:
        raise Exception("Unknown labeler type '{}'".format(labeler_type))


def _get_labeler(labeler_type):
    labelers = {}
    while 1:
        if labeler_type not in labelers:
            labelers[labeler_type] = _create_labeler(labeler_type)
        yield labelers[labeler_type]


def get_labeler_instance(labeler_type):
    return _get_labeler(labeler_type).__next__()


class Labeler:

    def generate_labels(self, strain_dataset):
        raise NotImplementedError


class StrainTypeLabeler(Labeler):

    name = 'type-labeler'

    def __init__(self):
        self.strain_type2color = {'hybrid': 'green', 'indica': 'purple', 'sativa': 'red'}

    def generate_labels(self, strain_dataset):
        for index in range(len(strain_dataset.datapoints)):
            # print(index)
            # print(strain_dataset.datapoint_index2_id[index])
            yield self.strain_type2color[strain_dataset.loc[strain_dataset.datapoint_index2_id[index]]['type']]


class Labeler(object):

    def __init__(self):
        pass

    def label(self, cluster):
        # val_getter = lambda x: 0 if 'Happy' not in x['effects'] else x['effects']['Happy']
        pass