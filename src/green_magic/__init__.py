import os
from .strain_dataset import StrainDataset
from .strainmaster import StrainMaster
from .clustering import ClusteringFactory, get_type_separation_eval

import logging

# strain_master = StrainMaster()
# clustering_factory = ClusteringFactory(strain_master)
extr_eval = get_type_separation_eval()

my_dir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.path.join(my_dir, 'gm.log'),
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


strain_logger = logging.getLogger('')

# Now, we can log to the root logger, or any other logger. First the root...
# logging.info('Blah blah')
