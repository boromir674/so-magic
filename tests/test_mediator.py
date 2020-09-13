
def test_mediator_scenario():
    from so_magic.utils import GenericMediator, BaseComponent
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
