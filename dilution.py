import math
from dataclasses import dataclass

# Constants
k_w = math.pow(10, -14)  # Water dissociation constant at 25°C
init_volume = 0.1  # Initial volume in liters
dilution_factor = 100
total_volume = init_volume * dilution_factor

@dataclass
class Solution:
    volume: float
    pH: float
    pOH: float = None

    def __post_init__(self):
        self.H_molarity = math.pow(10, -self.pH)
        self.H_mole = self.H_molarity * self.volume
        if self.pOH is None:
            self.pOH = -math.log10(k_w / self.H_molarity)
        self.OH_molarity = math.pow(10, -self.pOH)
        self.OH_mole = self.OH_molarity * self.volume

    @classmethod
    def from_H_mole(cls, volume: float, H_mole: float):
        H_molarity = H_mole / volume
        pH = -math.log10(H_molarity)
        return cls(volume, pH)
    
    def add_OH_info(self, OH_mole: float):
        self.OH_molarity = OH_mole / self.volume
        self.pOH = -math.log10(self.OH_molarity)


init_aq = Solution(volume=init_volume, pH=2)
diluent = Solution(volume=total_volume - init_aq.volume, pH=-math.log10(math.sqrt(k_w)))

total_aq = Solution.from_H_mole(volume=total_volume, H_mole=init_aq.H_mole + diluent.H_mole)
total_aq.add_OH_info(OH_mole=init_aq.OH_mole + diluent.OH_mole)

print(total_aq.pH)
print(total_aq.pOH)