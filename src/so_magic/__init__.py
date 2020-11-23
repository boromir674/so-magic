__version__ = '0.5.0'

from .so_master import SoMaster
from .data import init_data_manager
from .data.backend import init_backend

def init_so_magic():
    return SoMaster.create(init_data_manager(init_backend(engine_type='pd')))
