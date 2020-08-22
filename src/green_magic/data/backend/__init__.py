from .backend import Backend
from .engine import DataEngine
from .engine_specs import EngineSpecifications


PANDAS_ABBR = 'pd'
PANDAS_NAME = 'pandas'
from .panda_handling.df_backend import *

# create/register new empty/canvas engine
pd_engine = DataEngine.new(PANDAS_ABBR)

# create supporting object that can initialize an engine
pandas_engine_specs = EngineSpecifications(PANDAS_ABBR, PANDAS_NAME)

# initialize engine
pandas_engine_specs(pd_engine)

magic_backend = Backend(pd_engine)
