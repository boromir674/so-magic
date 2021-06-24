from .engine import Engine


def init_engine(engine_type='pd'):
    return Engine.from_backend(engine_type)
