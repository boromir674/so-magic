import attr
from green_magic.utils import Subject
from .self_organising_map import SomTrainer, SelfOrganizingMap


@attr.s
class SomFactory:
    """Implementing from the BaseSomFactory allows other class to register/subscribe on (emulated) 'events'.
       So, when the factory creates a new Som object, other entities can be notified."""
    trainer = attr.ib(init=True, default=SomTrainer())
    subject = attr.ib(init=True, default=Subject([]))

    def create_som(self, nb_cols, nb_rows, dataset, **kwargs):
        try:
            map_obj = self.trainer.infer_map(nb_cols, nb_rows, dataset, **kwargs)
            self.subject.state = map_obj
            self.subject.notify()
            return map_obj
        except NoFeatureVectorsError as e:
            logger.info(f"{e}. Fire up an 'encode' command.")
            raise e


@attr.s
class SelfOrganizingMapFactory:
    som_factory = attr.ib(init=True, default=SomFactory())

    def create(self, dataset, nb_cols, nb_rows, **kwargs):
        return SelfOrganizingMap(self.som_factory.create_som(nb_cols, nb_rows, dataset, **kwargs), dataset.name)


class NoFeatureVectorsError(Exception): pass
