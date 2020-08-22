from .data_manager import DataManager
from .backend import magic_backend
from .features.phi import PhiFunction

data_manager = DataManager(magic_backend)
PhiFunction.subject.attach(data_manager.built_phis)
