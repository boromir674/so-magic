import logging
import attr
from so_magic.utils import Subject
from .self_organising_map import SomTrainer, SelfOrganizingMap


logger = logging.getLogger(__name__)


@attr.s
class SelfOrganizingMapFactory:
    trainer = attr.ib(init=True, default=SomTrainer())
    subject = attr.ib(init=True, default=Subject([]))

    def create(self, dataset, nb_cols, nb_rows, **kwargs):
        try:
            # run a backend algorithm and get a self-organising map representation object
            somoclu_map = self.trainer.infer_map(nb_cols, nb_rows, dataset, **kwargs)
            self.subject.state = somoclu_map
            self.subject.notify()
            return SelfOrganizingMap(somoclu_map, dataset.name)
        except NoFeatureVectorsError as exception:
            logger.info("%s Fire up an 'encode' command.", str(exception))
            raise exception


class NoFeatureVectorsError(Exception): pass
