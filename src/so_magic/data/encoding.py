from abc import ABC, abstractmethod
import attr


class EncoderInterface(ABC):
    @abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError


@attr.s(slots=True)
class NominalAttributeEncoder(EncoderInterface, ABC):
    """Encode the observations of a categorical nominal variable.

    The client code can supply the possible values for the nominal variable, if known a priori.
    The possible values are stored in the 'values_set' attribute/property. If they are not supplied
    they should be computed at runtime (when running the encode method).

    It also defines and stores the string identifiers for each column produced in the 'columns attribute/property.

    Args:
        values_set (list): the possible values of the nominal variable observations, if known a priori
    """
    values_set: list = attr.ib(default=attr.Factory(list))
    columns: list = attr.ib(init=False, default=[])
