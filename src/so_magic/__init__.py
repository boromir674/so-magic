__version__ = '0.6.0'

from .so_master import SoMaster
from .data import init_data_manager
from .data.backend import init_backend
from .som import MagicMapManager
from .data.dataset import Dataset


def init_so_magic():
    return SoMaster(init_data_manager(init_backend(engine_type='pd')),
                    Dataset,
                    MagicMapManager)
