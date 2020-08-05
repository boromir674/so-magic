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


if __name__ == "__main__":
    # The client code.
    class ConcreteMediator(GenericMediator):
        def notify(self, sender: object, event: str) -> None:
            if event == "A":
                print("Mediator reacts on A and triggers following operations:")
                self._component2.do_c()
            elif event == "D":
                print("Mediator reacts on D and triggers following operations:")
                self._component1.do_b()
                self._component2.do_c()

    """
    Concrete Components implement various functionality. They don't depend on other
    components. They also don't depend on any concrete mediator classes.
    """
    class Component1(BaseComponent):
        def do_a(self) -> None:
            print("Component 1 does A.")
            self.mediator.notify(self, "A")

        def do_b(self) -> None:
            print("Component 1 does B.")
            self.mediator.notify(self, "B")


    class Component2(BaseComponent):
        def do_c(self) -> None:
            print("Component 2 does C.")
            self.mediator.notify(self, "C")

        def do_d(self) -> None:
            print("Component 2 does D.")
            self.mediator.notify(self, "D")
    

    c1 = Component1()
    c2 = Component2()
    my_mediator = ConcreteMediator(c1, c2)

    print("Client triggers operation A.")
    c1.do_a()

    print("\n", end="")

    print("Client triggers operation D.")
    c2.do_d()
