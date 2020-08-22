import pickle
import logging
from .strain_dataset import create_dataset_from_pickle
from .clustering import get_model_quality_reporter
from .data.dataset import DatapointsManager
from green_magic.utils import Invoker, CommandHistory
from .data.backend.engine import DataEngine

_log = logging.getLogger(__name__)


class StrainMaster:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            from green_magic.data.commands_manager import CommandsManager
            from green_magic.data.backend import Backend
            from green_magic.data.data_manager import DataManager
            from green_magic.data.backend import panda_handling

            print("!1111111", DataEngine.subclasses)

            cls.__instance = super().__new__(cls)
            DataEngine.new('pd')
            cls.__instance.data_api = DataManager(Backend(DataEngine.create('pd')))
            # make the datapoint_manager listen to newly created Datapoints objects events
            # cls.__instance.data_api.backend.engine.datapoints_factory.subject.attach(cls.__instance.data_api.backend.datapoints_manager)
        return cls.__instance

    def __call__(self, *args, **kwargs):
        """
        Call to update any of 'datasets_dir' and/or 'maps_dir'
        """
        self._datasets_dir = kwargs.get('datasets_dir', self._datasets_dir)
        self._maps_dir = kwargs.get('maps_dir', self._maps_dir)
        self.map_manager.maps_dir = self._maps_dir
        return self

    def __init__(self, datasets_dir=None, maps_dir=None): pass

    @property
    def commands(self):
        """Get a Command object from the pool of Command prototypes"""
        return self.data_api.command

    @property
    def datasets_dir(self):
        return self._datasets_dir

    @datasets_dir.setter
    def datasets_dir(self, dataset_directory_path):
        self._datasets_dir = dataset_directory_path
        # self.map_manager.maps_dir = dataset_directory_path

    def strain_names(self, coordinates):
        g = ((self.dt.datapoint_index2_id[_], self.som.bmus[_]) for _ in range(len(self.dt)))
        return [n for n, c in g if c[0] == coordinates['x'] and c[1] == coordinates['y']]

    @property
    def dt(self):
        """
        Returns the currently selected/active dataset as a reference to a StrainDataset object.\n
        :return: the reference to the dataset
        :rtype: green_magic.strain_dataset.StrainDataset
        """
        return self.data_api.backend.datapoints_manager.datapoints

        # if self.selected_dt_id not in self._id2dataset:
        #     raise InvalidDatasetSelectionError("Requested dataset with id '{}', but StrainMaster knows only of [{}].".format(self.selected_dt_id, ', '.join(self._id2dataset.keys())))
        # return self._id2dataset[self.selected_dt_id]

    @property
    def som(self):
        """
        Returns the currently selected/active som instance, as a reference to a som object.\n
        :return: the reference to the self-organizing map
        :rtype: somoclu.Somoclu
        """
        return self.map_manager.som

    @property
    def model_quality(self):
        return get_model_quality_reporter(self, self.selected_dt_id)

    def set_feature_vectors(self, list_of_variables=None):
        _ = self.get_feature_vectors(self.dt, list_of_variables=list_of_variables)

    def get_feature_vectors(self, strain_dataset, list_of_variables=None):
        """Call this function to get the encoded feature as a list of vectors
        This method must be called
        :param strain_dataset:
        :param list_of_variables:
        :return:
        """
        if not list_of_variables:
            return strain_dataset.load_feature_vectors()
        else:
            strain_dataset.use_variables(list_of_variables)
            return strain_dataset.load_feature_vectors()

    # def create_strain_dataset(self, jl_file, dataset_id, ffilter=''):
    #     data_set = StrainDataset(dataset_id)
    #     with open(jl_file, 'r') as json_lines_file:
    #         for line in json_lines_file:
    #             strain_dict = json.loads(line)
    #             if ffilter.split(':')[0] in strain_dict:
    #                 if strain_dict[ffilter.split(':')[0]] == ffilter.split(':')[1]:  # if datapoint meets criteria, add it
    #                     data_set.add(strain_dict)
    #                     if 'description' in strain_dict:
    #                         self.lexicon.munch(strain_dict['description'])
    #             else:
    #                 data_set.add(strain_dict)
    #                 if 'description' in strain_dict:
    #                     self.lexicon.munch(strain_dict['description'])
    #     data_set.load_feature_indexes()
    #     self._id2dataset[dataset_id] = data_set
    #     self.selected_dt_id = dataset_id
    #     _log.info("Created StrainDataset object with id '{}'".format(data_set.name))
    #     assert data_set.name == dataset_id
    #     return data_set

    def load_dataset(self, a_file):
        strain_dataset = create_dataset_from_pickle(self._datasets_dir + '/' + a_file)
        self._id2dataset[strain_dataset.name] = strain_dataset
        self.selected_dt_id = strain_dataset.name
        _log.info("Loaded dataset with id '{}'".format(strain_dataset.name))
        return strain_dataset

    def save_active_dataset(self):
        self.save_dataset(self.selected_dt_id)

    def save_dataset(self, strain_dataset_id):
        dataset = self._id2dataset[strain_dataset_id]
        if dataset.has_missing_values:
            name = '-not-clean'
        else:
            name = '-clean'
        name = self._datasets_dir + '/' + dataset.name + name + '.pk'
        try:
            with open(name, 'wb') as pickled_dataset:
                pickle.dump(dataset, pickled_dataset, protocol=pickle.HIGHEST_PROTOCOL)
            _log.info("Saved dataset with id '{}' as {}".format(strain_dataset_id, name))
        except RuntimeError as e:
            _log.debug(e)
            _log.info("Failed to save dataset wtih id {}".format(strain_dataset_id))

    def __getitem__(self, wd_id):
        self.selected_dt_id = wd_id
        return self


class InvalidDatasetSelectionError(Exception): pass
