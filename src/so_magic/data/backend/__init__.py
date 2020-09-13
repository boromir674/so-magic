from .backend import Backend
from .engine import DataEngine
from .engine_specs import EngineSpecifications

ENGINES = {
    'pd': {
        'abbr': 'pd',
        'name': 'pandas',
    },
}

def init_backend(engine_type='pd'):
    from so_magic.data.backend.panda_handling.df_backend import PDTabularRetriever, PDTabularIterator, PDTabularMutator
    # create/register new empty/canvas engine
    pd_engine = DataEngine.new(ENGINES[engine_type]['abbr'])

    # create supporting object that can initialize an engine
    pandas_engine_specs = EngineSpecifications(ENGINES[engine_type]['abbr'], ENGINES[engine_type]['name'])

    # initialize engine
    pandas_engine_specs(pd_engine)

    magic_backend = Backend(pd_engine)
    pd_engine.backend = magic_backend

    return magic_backend
