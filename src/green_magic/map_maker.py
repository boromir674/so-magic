import inspect
import logging
import os
import subprocess
import sys

import numpy as np
import somoclu
from sklearn.cluster import KMeans

_log = logging.getLogger(__name__)


class MapMakerManager:

    def __init__(self, strain_master, graphs_dir):
        self._strain_master = strain_master
        self.graphs_dir = graphs_dir
        self.implemented_map_makers = ['somoclu']
        self.map_makers = {}
        self.id2map_obj = {}
        self.map_obj2id = {}
        self.som = None
        self.figures = {}
        self.backend = 'somoclu'
        self._nb_rows = None
        self._nb_cols = None
        self._dataset_id = ''
        self.mpeta = os.path.dirname(os.path.realpath(__file__)) + '/../../graphs/'
        for figure in os.listdir(self.graphs_dir):
            self.figures[figure.split('.')[0]] = self.mpeta + figure
    @property
    def maps_dir(self):
        return self.graphs_dir
    @maps_dir.setter
    def maps_dir(self, maps_directory_path):
        self.graphs_dir = maps_directory_path

    def __getitem__(self, map_expr):
        return self.get_map_maker(self.backend, self._strain_master.selected_dt_id, int(map_expr.split('x')[0]), int(map_expr.split('x')[1]))

    def get_map_maker(self, map_type, dataset_id, nb_rows, nb_cols):
        self.backend = map_type
        self._nb_rows = nb_rows
        self._nb_cols = nb_cols
        self._dataset_id = dataset_id

        _id = self._get_map_maker_id(self.backend)
        if _id not in self.map_makers:
            self.map_makers[_id] = self._create_map_maker(map_type, self._strain_master._id2dataset[dataset_id], nb_rows=nb_rows, nb_cols=nb_cols)
            self.map_makers[_id].register(self)
        return self

    def update(self, *args, **kwargs):
        map_id = '{}_{}_'.format(self.backend, self._dataset_id) + '_'.join(args)
        self.id2map_obj[map_id] = kwargs['map_object']
        self.som = kwargs['map_object']
        self.map_obj2id[self.som] = map_id

    def get_som(self, map_expr):
        d = decode(map_expr)
        map_id = self.get_map_id(d['map-type'], d['grid-type'], d['nb-rows'], d['nb-cols'], initialization=d['initialization'], clusters=False)
        if map_id not in self.id2map_obj:
            map_maker = self.get_map_maker(self.backend, self._strain_master.selected_dt_id, nb_rows=d['nb-rows'], nb_cols=d['nb-cols']).map_makers[self._get_map_maker_id(self.backend)]
            som = map_maker.create_map(d['map-type'], d['grid-type'], initialization=d['initialization'])
            _log.info('Created som object with id: {}'.format(map_id))
        else:
            _log.info('Loaded som object with id: {}'.format(map_id))
            return self.id2map_obj[map_id]
        return som

    def show_map(self, som_obj):
        """
        Opens the default image viewer and shows the visualization of the given trained self-organizing map object.
        Saves the created png file in the 'self.graphs_dir' path.\n
        :param som_obj: a trained instance of a self-organizing map
        :type som_obj: somoclu.Somoclu
        """
        if not isinstance(som_obj, somoclu.Somoclu):
            warnings.warn("Received {} object instead of Somoclu", DeprecationWarning)
            return None
        cl = False
        if som_obj.clusters is not None:
            cl = np.max(som_obj.clusters)
        map_id = self.get_map_id(som_obj._map_type, som_obj._grid_type, som_obj._n_rows, som_obj._n_columns, initialization=som_obj._initialization, clusters=cl)
        figure_path = self.graphs_dir + '/' + map_id
        som_obj.view_umatrix(bestmatches=True, filename=figure_path)
        subprocess.call(['xdg-open', figure_path + '.png'])


    def _create_map_maker(self, map_maker_type, weed_dataset, nb_rows=20, nb_cols=20):
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if hasattr(obj, 'name') and map_maker_type == obj.name:
                    return obj(nb_rows, nb_cols, weed_dataset, name)
        else:
            raise Exception("Unknown map maker type '%s'" % map_maker_type)

    def get_map_id(self, map_type, grid_type, nb_rows, nb_cols, initialization='', clusters=False):
        b = '_'.join([self.backend, self._strain_master.selected_dt_id, initialization, map_type, grid_type, str(nb_rows), str(nb_cols)])
        if clusters:
            return b + '_cl' + str(clusters)
        else:
            return b

    def _get_map_maker_id(self, backend):
        return '_'.join([backend, self._strain_master.selected_dt_id, str(self._nb_rows), str(self._nb_cols)])


def decode(map_expr):
    d = {}
    els = map_expr.split('.')
    d['map-type'] = els[0]
    d['grid-type'] = els[1]
    d['nb-rows'] = int(els[2])
    d['nb-cols'] = int(els[3])
    if len(els) < 5:
        d['initialization'] = ''  # random intialization of codebook of shape (nb_neurons, dims)
    else:
        d['initialization'] = els[4]  # pca
    return d


class MapMaker:

    def __init__(self, nb_rows, nb_cols, strain_dataset, name):
        """
        :type strain_dataset: strain_dataset.StrainDataset
        """
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self._strain_dataset = strain_dataset
        self.name = name
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def update_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def create_map(self, map_type, grid_type, initialization=None):
        try:
            map_obj = self._create_map(map_type, grid_type, initialization=initialization)
        except NoDatapointsException:
            _log.info("No datapoints vectors found in {}. Call the 'get_feature_vectors' of strain_master".format(self._strain_dataset.name))
            return None
        ini = ''
        if initialization is not None:
            ini = initialization
        self.update_observers(ini, map_type, grid_type, str(self.nb_rows), str(self.nb_cols), map_object=map_obj)
        return map_obj

    def save_map_as_figure(self, map_obj, a_name, **kwargs):
        raise NotImplementedError

    def _create_map(self, map_type, grid_type, initialization=None):
        raise NotImplementedError


class SomocluMapMaker(MapMaker):

    name = 'somoclu'

    def __init__(self, nb_rows, nb_cols, data, name):
        super().__init__(nb_rows, nb_cols, data, name)

    def _create_map(self, map_type, grid_type, initialization=None):
        if not self._strain_dataset.datapoints:
            raise NoDatapointsException
        if initialization != 'pca':
            initialization = None
        som = somoclu.Somoclu(self.nb_cols, self.nb_rows, maptype=map_type, gridtype=grid_type, initialization=initialization, compactsupport=False)

        som.train(data=np.array(self._strain_dataset.datapoints, dtype=np.float32))
        return som

    def save_map_as_figure(self, map_obj, a_name, colors=None, labels=None, clusters=False, random_state=None):
        if clusters:
            map_obj.cluster(algorithm=KMeans(n_clusters=clusters, random_state=random_state))
            map_obj.view_umatrix(bestmatches=True, bestmatchcolors=colors, labels=labels, filename=a_name)
        else:
            map_obj.view_umatrix(bestmatches=True, bestmatchcolors=colors, labels=labels, filename=a_name)


def print_vector(feature_encoded_vector):
    print('[ ' + ' '.join(str(el) for el in map(lambda x: str(x if type(x) == int else '%.2f' % x), feature_encoded_vector)) + ' ]')


class NoDatapointsException(Exception):
    pass
