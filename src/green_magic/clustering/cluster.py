from collections import Counter, OrderedDict


@attr.s
class Grouping:
    """A Cluster is basically a group of objects"""
    members = attr.ib(init=True, converter=tuple)

    def __str__(self):
        return f'len {len(self.members)}'

    def __len__(self):
        return len(list(self.members))

    def __iter__(self):
        return iter(self.members)

    def gen_members(self, **kwargs):
        """
        Accepts 'sort' True/False and 'reverse': True/False
        """
        return iter({True: sorted, False: self.__pass}[kwargs.pop('sort', False)](self.members, **kwargs))

    def __pass(self, x, **kwargs):
        return x

@attr.s
class BaseCluster(Grouping):
    """
    An instance of this class encapsuates the behaviour of a single (one group) cluster estimated on some data. The object contains
    essentially a "list" of objects
    """
    def alphabetical(self):
        return self.gen_members(sort=True)

def _is_coordinate_value(self, attribute, value):
    if value < 0:
        raise ValueError("Expected the input coordinate to be a positive number.")

@attr.s
class Coordinates:
    x = attr.ib(init=True, validator=_is_coordinate_value)
    y = attr.ib(init=True, validator=_is_coordinate_value)

    @staticmethod
    def from_duo(two_element_list_like):
        return Coordinates(*list(iter(two_element_list_like)))

@attr.s
class SOMCluster(BaseCluster):
    """
    An instance of this class encapsulates the behaviour of a clustering computed on a self-organizing map. A cluster computed on
    a trained SOM, is located on a neuron
    is located on one of the neurons (bmus)
    """
    # coordinates = attr.ib(init=True, converter=Coordinates.from_duo)
    id = attr.ib(init=True, default=None)
