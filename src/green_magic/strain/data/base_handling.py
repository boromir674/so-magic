from abc import ABCMeta, abstractmethod


class DataHandlerInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_all_variables(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_categorical_variables(self, *args, **kwargs):
        """call this to get the categorical/discrete variables; either 'nominal' or 'ordinal'"""
        raise NotImplementedError

    @abstractmethod
    def get_numerical_variables(self, *args, **kwargs):
        """call this to get the numerical/continuous variables; either 'interval' or 'ratio'"""
        raise NotImplementedError


class DataHandler(DataHandlerInterface, metaclass=ABCMeta):
    subclasses = {}
    @classmethod
    def register_as_subclass(cls, handler_type):
        def wrapper(subclass):
            cls.subclasses[handler_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, handler_type, *args, **kwargs):
        if handler_type not in cls.subclasses:
            raise ValueError('Bad "DataHandler" type \'{}\''.format(handler_type))
        return cls.subclasses[handler_type](*args, **kwargs)


class BaseDataHandler(DataHandler):

    def add_state(self, dataset, feature, computer, state, cache_prev=True, **kwargs):
        pass

    def del_state(self, dataset, feature, state, **kwargs):
        pass

    def get_all_variables(self, *args, **kwargs):
        return args[0].columns

    def get_categorical_variables(self, *args, **kwargs):
        pass

    def get_numerical_variables(self, *args, **kwargs):
        pass

    def missing(self, *args, **kwargs):
        pass
