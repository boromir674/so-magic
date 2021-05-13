from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """Standalone command, encapsulating all logic and data needed, required for execution."""
    @abstractmethod
    def execute(self) -> None:
        """Execute the command; run the commands logic."""
        raise NotImplementedError
