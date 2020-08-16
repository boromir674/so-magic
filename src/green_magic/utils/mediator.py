from abc import ABC, abstractmethod, ABCMeta

__all__ = ['GenericMediator', 'BaseComponent']


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """
    @abstractmethod
    def notify(self, sender: object, event: str) -> None:
        """[summary]

        Args:
            sender (object): [description]
            event (str): [description]
        """
        raise NotImplementedError


class GenericMediator(Mediator, metaclass=ABCMeta):
    """Abstract Mediator class that automatically configures components received as *args through the constructor.
    """
    def __new__(cls, *components, **kwargs):
        x = super().__new__(cls)
        for i, component in enumerate(components):
            setattr(x, f'_component{i+1}', component)
            getattr(x, f'_component{i+1}').mediator = x
        return x


class BaseComponent:
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator
