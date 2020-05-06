# import attr
#
# @attr.s
# class ObjectsPool:
#     constructor = attr.ib(init=True)
#     _objects = {}
#
#     def get_object(self, *args, **kwargs):
#         key = self._build_hash(*args, **kwargs)
#         if key not in ObjectsPool._objects:
#             ObjectsPool._objects[key] = self.constructor(*args, **kwargs)
#         return ObjectsPool._objects[key]
#
#     def _build_hash(self, *args, **kwargs):
#         return hash('-'.join([str(_) for _ in args]))
#
#
# class MapObjectsPool(ObjectsPool):
#     def _build_hash(self, *args, **kwargs):
#         if type(args[0]) == str:
#             return super()._build_hash(args[0])
#         return super()._build_hash(*args)
#
#
# class AbstractSomFactory:
#
#     def create_som(self, *args, **kwargs):
#         raise NotImplementedError
#
#
# @attr.s
# class BaseSomFactory:
#     """Implementing from the BaseSomFactory allows other class to register/subscribe on (emulated) 'events'."""
#     observers = attr.ib(init=False, default=[])
#
#     def register(self, observer):
#         if observer not in self.observers:
#             self.observers.append(observer)
#
#     def unregister(self, observer):
#         if observer in self.observers:
#             self.observers.remove(observer)
#
#     def unregister_all(self):
#         if self.observers:
#             del self.observers[:]
#
#     def update_observers(self, *args, **kwargs):
#         for observer in self.observers:
#             observer.update(*args, **kwargs)
#
#
# import logging
# logger = logging.getLogger(__name__
#
#                            )
# @attr.s
# class SomFactory(BaseSomFactory):
#     trainer = attr.ib(init=True)
#
#     def create_som(self, *args, **kwargs):
#         try:
#             map_obj = self.trainer.train_map(*args[:3], **kwargs)
#             self.update_observers(*args, self.nb_rows, self.nb_cols, map_object=map_obj)
#             return map_obj
#         except NoDatapointsException:
#             logger.info(f"No datapoints vectors found in dataset {self.dataset}. Fire up an 'encode' command.")
#
#
# import numpy as np
#
# @attr.s
# class SomTrainer(BaseSomeTrainer):
#
#     def train_map(self, nb_cols, nb_rows, dataset, **kwargs):
#         """Infer a self-organizing map from dataset.\n
#         initialcodebook = None, kerneltype = 0, maptype = 'planar', gridtype = 'rectangular',
#         compactsupport = False, neighborhood = 'gaussian', std_coeff = 0.5, initialization = None
#         """
#         if not dataset.datapoints:
#             raise NoFeatureVectors
#         som = somoclu.Somoclu(nb_cols, nb_rows, **kwargs)
#         som.train(data=np.array(dataset.datapoints, dtype=np.float32))
#         return som
#
# class NoFeatureVectors(Exception): pass
#
#
# @attr.s
# class MapFactory:
#     factory = attr.ib(init=True)
#     pool = attr.ib(init=False, default=attr.Factory(lambda self: MapObjectsPool(self.factory.create_som), takes_self=True))
#
#     def get_som(self, *args, **kwargs):
#         return self.pool.get_object(*args, **kwargs)
#
#
# @attr.s
# class SomManager:
#     graphs_dir = attr.ib(init=True)
#     backend = attr.ib(init=True, default='somoclu')
#
#     factories = {'somoclu': MapFactory(SomFactory(SomTrainer()))}
#
#     def get_som(self, *args, **kwargs):
#         return self.factories[self.backend].create_som(*args, **kwargs)
#
#     @property
#     def factory(self):
#         return self.factories[self.backend]
#
#     mpeta = os.path.dirname(os.path.realpath(__file__)) + '/../../graphs/'
#
#
# class MapMakerManager:
#
#     def __init__(self, strain_master, graphs_dir):
#         self._strain_master = strain_master
#         self.graphs_dir = graphs_dir
#         self.implemented_map_makers = ['somoclu']
#         self.map_makers = {}
#         self.id2map_obj = {}
#         self.map_obj2id = {}
#         self.som = None
#         self.figures = {}
#         self.backend = 'somoclu'
#         self._nb_rows = None
#         self._nb_cols = None
#         self._dataset_id = ''
#         self.mpeta = os.path.dirname(os.path.realpath(__file__)) + '/../../graphs/'
#         for figure in os.listdir(self.graphs_dir):
#             self.figures[figure.split('.')[0]] = self.mpeta + figure
#     @property
#     def maps_dir(self):
#         return self.graphs_dir
#     @maps_dir.setter
#     def maps_dir(self, maps_directory_path):
#         self.graphs_dir = maps_directory_path
#
#     def __getitem__(self, map_expr):
#         return self.get_map_maker(self.backend, self._strain_master.selected_dt_id, int(map_expr.split('x')[0]), int(map_expr.split('x')[1]))
#
#     def get_map_maker(self, map_type, dataset_id, nb_rows, nb_cols):
#         self.backend = map_type
#         self._nb_rows = nb_rows
#         self._nb_cols = nb_cols
#         self._dataset_id = dataset_id
#
#         _id = self._get_map_maker_id(self.backend)
#         if _id not in self.map_makers:
#             self.map_makers[_id] = self._create_map_maker(map_type, self._strain_master._id2dataset[dataset_id], nb_rows=nb_rows, nb_cols=nb_cols)
#             self.map_makers[_id].register(self)
#         return self
#
#     def update(self, *args, **kwargs):
#         map_id = '{}_{}_'.format(self.backend, self._dataset_id) + '_'.join(args)
#         self.id2map_obj[map_id] = kwargs['map_object']
#         self.som = kwargs['map_object']
#         self.map_obj2id[self.som] = map_id
#
#     def get_som(self, map_expr):
#         d = decode(map_expr)
#         map_id = self.get_map_id(d['map-type'], d['grid-type'], d['nb-rows'], d['nb-cols'], initialization=d['initialization'], clusters=False)
#         if map_id not in self.id2map_obj:
#             map_maker = self.get_map_maker(self.backend, self._strain_master.selected_dt_id, nb_rows=d['nb-rows'], nb_cols=d['nb-cols']).map_makers[self._get_map_maker_id(self.backend)]
#             som = map_maker.create_map(d['map-type'], d['grid-type'], initialization=d['initialization'])
#             _log.info('Created som object with id: {}'.format(map_id))
#         else:
#             _log.info('Loaded som object with id: {}'.format(map_id))
#             return self.id2map_obj[map_id]
#         return som
#
#     def show_map(self, som_obj):
#         """
#         Opens the default image viewer and shows the visualization of the given trained self-organizing map object.
#         Saves the created png file in the 'self.graphs_dir' path.\n
#         :param som_obj: a trained instance of a self-organizing map
#         :type som_obj: somoclu.Somoclu
#         """
#         if not isinstance(som_obj, somoclu.Somoclu):
#             warnings.warn("Received {} object instead of Somoclu", DeprecationWarning)
#             return None
#         cl = False
#         if som_obj.clusters is not None:
#             cl = np.max(som_obj.clusters)
#         map_id = self.get_map_id(som_obj._map_type, som_obj._grid_type, som_obj._n_rows, som_obj._n_columns, initialization=som_obj._initialization, clusters=cl)
#         figure_path = self.graphs_dir + '/' + map_id
#         som_obj.view_umatrix(bestmatches=True, filename=figure_path)
#         subprocess.call(['xdg-open', figure_path + '.png'])
#
#
#     def _create_map_maker(self, map_maker_type, weed_dataset, nb_rows=20, nb_cols=20):
#         for name, obj in inspect.getmembers(sys.modules[__name__]):
#             if inspect.isclass(obj):
#                 if hasattr(obj, 'name') and map_maker_type == obj.name:
#                     return obj(nb_rows, nb_cols, weed_dataset, name)
#         else:
#             raise Exception("Unknown map maker type '%s'" % map_maker_type)
#
#     def get_map_id(self, map_type, grid_type, nb_rows, nb_cols, initialization='', clusters=False):
#         b = '_'.join([self.backend, self._strain_master.selected_dt_id, initialization, map_type, grid_type, str(nb_rows), str(nb_cols)])
#         if clusters:
#             return b + '_cl' + str(clusters)
#         else:
#             return b
#
#     def _get_map_maker_id(self, backend):
#         return '_'.join([backend, self._strain_master.selected_dt_id, str(self._nb_rows), str(self._nb_cols)])
