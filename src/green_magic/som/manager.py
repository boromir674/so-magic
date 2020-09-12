import attr
import logging

from green_magic.utils import ObjectsPool
from .factory import SelfOrganizingMapFactory

logger = logging.getLogger(__name__)


class SomapObjectPool(ObjectsPool):
    def _build_hash(self, *args, **kwargs):
        return str(MapId(*args, kwargs.get('initialization'), kwargs.get('map_type'), kwargs.get('grid_type')))


@attr.s
class MapManager:
    map_factory = attr.ib(init=True, default=SelfOrganizingMapFactory())
    pool = attr.ib(init=False, default=attr.Factory(lambda self: SomapObjectPool(self.map_factory.create), takes_self=True))

    def get_map(self, *args, **kwargs):
        """
        'dataset', 'nb_cols', 'nb_rows', 'initialization', 'map_type', 'grid_type'
        """
        return self.pool.get_object(*args, **kwargs)

    def train(self, dataset, nb_cols, nb_rows, **kwargs):
        """"""
        return self.map_factory.create(dataset, nb_cols, nb_rows, **kwargs)


@attr.s
class MagicMapManager:
    so_master = attr.ib(init=True)
    manager = attr.ib(init=False, default=MapManager())

    def train(self, nb_cols, nb_rows, **kwargs):
        return self.manager.train(self.so_master.dataset, nb_cols, nb_rows, **kwargs)


@attr.s
class MapId:
    dataset_name = attr.ib(init=True)
    _n_columns = attr.ib(init=True)
    _n_rows = attr.ib(init=True)
    initialization = attr.ib(init=True)
    map_type = attr.ib(init=True)
    grid_type = attr.ib(init=True)

    @staticmethod
    def from_self_organizing_map(somap, **kwargs):
        return MapId(kwargs.get('dataset_name', somap.dataset_name), *[getattr(somap, attribute.name) for attribute in MapId.__attrs_attrs__[1:]])

    def __dir__(self):
        return sorted([attribute.name for attribute in self.__attrs_attrs__])

    def __iter__(self):
        """Default implementation of __iter__ to allow dict(self) in client code"""
        return iter([(k, getattr(self, k)) for k in self.__dir__()])

    def __str__(self):
        return '-'.join(str(getattr(self, _)) for _ in dir(self))


if __name__ == '__main__':
    map_manager = MapManager()

