from .tick_obj import TickObject

class Tick(TickObject):
    def __init__(self,symbols=None) -> None:
        super().__init__(symbols=symbols)
