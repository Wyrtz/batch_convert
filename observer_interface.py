from abc import ABC, abstractmethod

class Observer():
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, message: tuple) -> None:
        """
        Receive update from subject.
        """
        pass
