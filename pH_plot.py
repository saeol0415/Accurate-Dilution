import math
import numpy as np
import matplotlib.pyplot as plt
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

    def __post_init__(self):
        self.H_molarity = math.pow(10, -self.pH)
        self.H_mole = self.H_molarity * self.volume

    @classmethod
    def from_mole(cls, volume: float, H_mole: float):
        H_molarity = H_mole / volume
        pH = -math.log10(H_molarity)
        return cls(volume, pH)

# Function to calculate total pH after dilution
def calculate_total_pH(init_pH):
    init_aq = Solution(volume=init_volume, pH=init_pH)
    diluent = Solution(volume=total_volume - init_aq.volume, pH=-math.log10(math.sqrt(k_w)))

    total_aq = Solution.from_mole(volume=total_volume, H_mole=init_aq.H_mole + diluent.H_mole)

    return total_aq.pH

initial_pH_values = np.linspace(0, 14, 100)
final_pH_values = [calculate_total_pH(pH) for pH in initial_pH_values]

plt.plot(initial_pH_values, final_pH_values)
plt.title("Initial pH vs Final pH after 100x dilution")
plt.xlabel("Initial pH")
plt.ylabel("Final pH")
plt.xlim(0, 14)
plt.xticks(np.arange(0, 15, 1))
plt.grid()
plt.show()