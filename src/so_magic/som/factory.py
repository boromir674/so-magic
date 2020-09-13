import attr
from so_magic.utils import Subject
from .self_organising_map import SomTrainer, SelfOrganizingMap


@attr.s
class SelfOrganizingMapFactory:
    trainer = attr.ib(init=True, default=SomTrainer())
    subject = attr.ib(init=True, default=Subject([]))

    def create(self, dataset, nb_cols, nb_rows, **kwargs):
        try:
            map_obj = self.trainer.infer_map(nb_cols, nb_rows, dataset, **kwargs)  # backend dependent (eg somoclu kind of object)
            self.subject.state = map_obj
            self.subject.notify()
            return SelfOrganizingMap(map_obj, dataset.name)
        except NoFeatureVectorsError as e:
            logger.info(f"{e}. Fire up an 'encode' command.")
            raise e


class NoFeatureVectorsError(Exception): pass
