"""Define a wrapper around an Engine as the Backend class which constructor can initialize Backend instances."""
import attr
from so_magic.data.magic_datapoints_factory import BroadcastingDatapointsFactory
from so_magic.data.datapoints_manager import DatapointsManager


@attr.s
class Backend:
    """Wrapper of a data engine, a datapoints manager and a datapoints factory.

    Instances of this class act as data placeholders (aka data classes) and take at runtime a data engine (eg a set of
    pandas-dependent implementations of the "Tabular Data interfaces" defined in so_magic.data.interfaces).

    Args:
        engine_instance (DataEngine): a data engine represented as a class object (eg class MyClass: pass)
    """
    engine_instance = attr.ib(init=True)
    datapoints_manager = attr.ib(init=False, default=attr.Factory(DatapointsManager))
    datapoints_factory = attr.ib(init=True, default=attr.Factory(BroadcastingDatapointsFactory))

    @property
    def engine(self):
        """The Data Engine instance, that this object wraps around.

        Returns:
            DataEngine: the Data Engine instance object
        """
        return self.engine_instance

    @engine.setter
    def engine(self, engine):
        """Set the Data Engine instance to the input engine object.

        Args:
            engine (DataEngine): the Data Engine object to set with
        """
        self.engine_instance = engine
