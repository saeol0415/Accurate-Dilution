import math
from dataclasses import dataclass

# Constants
k_w = math.pow(10, -14)  # Water dissociation constant at 25°C
init_volume = 0.01  # Initial volume in liters
dilution_factor = 100
total_volume = init_volume * dilution_factor

@dataclass
class Solution:
    volume: float
    pH: float

    def __post_init__(self):
        self.H_molarity = math.pow(10, -self.pH)
        self.H_mole = self.H_molarity * self.volume

    @classmethod
    def from_H_mole(cls, volume: float, H_mole: float):
        H_molarity = H_mole / volume
        pH = -math.log10(H_molarity)
        return cls(volume, pH)


init_aq = Solution(volume=init_volume, pH=6)
diluent = Solution(volume=total_volume - init_aq.volume, pH=-math.log10(math.sqrt(k_w)))

total_aq = Solution.from_H_mole(volume=total_volume, H_mole=init_aq.H_mole + diluent.H_mole)

print(total_aq.pH)