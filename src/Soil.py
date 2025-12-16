from enum import Enum

class Soil(Enum):
    MOOR = ("Moor", 0)
    CLAY = ("Clay", 0)
    CLAY_SAND = ("Clay Sand", 0)
    FINE_SAND = ("Fine Sand", 0)
    MIDDLE_SAND = ("Middle Sand", 0)
    CHUNK_SAND = ("Chunk Sand", 0)
    GRAVEL = ("Gravel", 0)
    ROCK = ("Rock", 1)

    def __init__(self, label, infiltration_rate):
        self.label = label
        self.infiltration_rate = infiltration_rate

    @property
    def infiltration(self):
        return self.infiltration_rate

    @infiltration.setter
    def infiltration(self, value):
        """Update the infiltration rate for this soil type."""
        if value < 0:
            raise ValueError("Infiltration rate cannot be negative.")
        self._infiltration_rate = value

    def __str__(self):
        return self.label
