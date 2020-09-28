import attr

@attr.s
class LinearScale:
    lower_bound = attr.ib(init=True, type=int)
    upper_bound = attr.ib(init=True, type=int)

    @upper_bound.validator
    def __validate_scale(self, attribute, upper_bound):
        if upper_bound <= self.lower_bound:
            raise ValueError(
                f'The linear scale, should have lower_bound < upper_bound. Instead lower_bound={self.lower_bound}, upper_bound={upper_bound}')

    def __len__(self):
        """Returns 2, since the lower and upper bound values are sufficient to define a linear scale."""
        return 2

    @classmethod
    def create(cls, two_element_list_like):
        return LinearScale(*[_ for _ in two_element_list_like])


@attr.s
class MapOnLinearSpace:
    _from_scale = attr.ib(init=True, type=LinearScale)
    _target_scale = attr.ib(init=True, type=LinearScale)
    _reverse = attr.ib(init=True, default=False, type=bool)
    _transform_callback = attr.ib(init=False,
                                  default=attr.Factory(lambda self: self._get_transform_callback(), takes_self=True))

    @classmethod
    def universal_constructor(cls, from_scale, target_scale, reverse=False):
        return MapOnLinearSpace(LinearScale.create(from_scale),
                                LinearScale.create(target_scale),
                                reverse)

    def __transform_inverted(self, number):
        # F(x) = { ( to_scale_min - to_scale_max ) * x + to_scale_max * from_scale_max - to_scale_min * from_scale_min }  / ( from_scale_max - from_scale_min )
        return ( (self._target_scale.lower_bound - self._target_scale.upper_bound) * number + self._target_scale.upper_bound * self._from_scale.upper_bound - self._target_scale.lower_bound * self._from_scale.lower_bound ) / (
               self._from_scale.upper_bound - self._from_scale.lower_bound)

    def __transform(self, number):
        return ((self._target_scale.upper_bound - self._target_scale.lower_bound) * number + self._target_scale.lower_bound * self._from_scale.upper_bound - self._target_scale.lower_bound * self._from_scale.lower_bound) / (self._from_scale.upper_bound - self._from_scale.lower_bound)

    def _get_transform_callback(self):
        if self._reverse:
            return self.__transform_inverted
        return self.__transform

    def transform(self, number):
        """Transform the input number to a different linear scale."""
        return self._transform_callback(number)

    @property
    def from_scale(self):
        return self._from_scale

    @from_scale.setter
    def from_scale(self, from_scale):
        self._from_scale = LinearScale.create(from_scale)
        self._transform_callback = self._get_transform_callback()

    @property
    def target_scale(self):
        return self._target_scale

    @target_scale.setter
    def target_scale(self, target_scale):
        self._target_scale = LinearScale.create(target_scale)
        self._transform_callback = self._get_transform_callback()

    @property
    def reverse(self):
        return self._reverse

    @reverse.setter
    def reverse(self, reverse):
        self._reverse = reverse
        self._transform_callback = self._get_transform_callback()
