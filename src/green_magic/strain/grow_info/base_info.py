
@attr.s
class GrowInfo:
    subclasses = {}

    @classmethod
    def register_subclass(cls, grow_info_subcategory):
        def decorator(subclass):
            cls.subclasses[grow_info_subcategory] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, grow_info_subcategory, *args, **kwargs):
        if grow_info_subcategory not in cls.subclasses:
            raise ValueError('Bad grow_info_subcategory \'{}\''.format(grow_info_subcategory))
        return cls.subclasses[grow_info_subcategory](*args, **kwargs)

    @classmethod
    def _construct(cls, grow_info_subcategory, *args, **kwargs):
        if grow_info_subcategory not in cls.subclasses:
            raise ValueError('Bad grow_info_subcategory \'{}\''.format(grow_info_subcategory))
        return cls.subclasses[grow_info_subcategory](*args, **kwargs)



