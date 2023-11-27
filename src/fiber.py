import numpy as np

# info about fiber sensor
class FiberState:
    NONE = 0
    GAS = 1
    WATER = 2
    WAVE = 3
    BUBBLE = 4
    SLUG = 5
    
class Fiber:
    def _init_(self, x, y) -> None:
        self.x = x
        self.y = y
        self.sequence = list

    def set_signal_sequence(self, normalization_seq):
        self.sequence = normalization_seq

    def get_signal_sequence(self):
        return self.sequence
    
    def get_next_sginal(self):
        signal = None
        if len(self.sequence) != 0:
            self.sequence[0]
            self.sequence = self.sequence[1:]

        return signal
    
    # ... 