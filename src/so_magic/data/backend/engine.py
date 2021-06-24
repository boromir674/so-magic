"""Define a wrapper around an Engine as the Backend class which constructor can initialize Backend instances."""
import attr
from so_magic.data.datapoints_manager import DatapointsManager
from so_magic.data.backend.panda_handling.df_backend import magic_backends


@attr.s
class Engine:
    """Wrapper of a data engine, a datapoints manager and a datapoints factory.

    Instances of this class act as data placeholders (aka data classes) and take at runtime a data engine (eg a set of
    pandas-dependent implementations of the "Tabular Data interfaces" defined in so_magic.data.interfaces).

    Args:
        engine_instance (DataEngine): a data engine represented as a class object (eg class MyClass: pass)
    """
    backend_instance = attr.ib(init=True)
    backends = attr.ib(init=True, default=attr.Factory(magic_backends))
    datapoints_manager = attr.ib(init=False, default=attr.Factory(DatapointsManager))

    @property
    def backend(self):
        """The Data Engine instance, that this object wraps around.

        Returns:
            DataEngine: the Data Engine instance object
        """
        return self.backend_instance

    @backend.setter
    def backend(self, engine):
        """Set the Data Engine instance to the input engine object.

        Args:
            engine (DataEngine): the Data Engine object to set with
        """
        self.backend_instance = engine

    @staticmethod
    def from_backend(backend_id: str):
        engine = Engine(None)
        engine.backend = engine.backends.backends[backend_id]
        return engine
