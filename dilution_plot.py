import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Constants
k_w = math.pow(10, -14)  # Water dissociation constant at 25°C
init_volume = 0.1  # Initial volume in liters

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
    def from_mole(cls, volume: float, H_mole: float):
        H_molarity = H_mole / volume
        pH = -math.log10(H_molarity)
        return cls(volume, pH)

    def add_OH_info(self, OH_mole: float):
        self.OH_molarity = OH_mole / self.volume
        self.pOH = -math.log10(self.OH_molarity)

# Function to calculate total pH and pOH after dilution
def calculate_total_pH_pOH(init_pH, dilution_factor):
    total_volume = init_volume * dilution_factor
    init_aq = Solution(volume=init_volume, pH=init_pH)
    diluent = Solution(volume=total_volume - init_aq.volume, pH=-math.log10(math.sqrt(k_w)))

    total_aq = Solution.from_mole(volume=total_volume, H_mole=init_aq.H_mole + diluent.H_mole)
    total_aq.add_OH_info(OH_mole=init_aq.OH_mole + diluent.OH_mole)

    return total_aq.pH, total_aq.pOH


initial_pH_values = np.linspace(0, 14, 100)
dilution_factors = [10, 100, 1000, 10000]

fig, ((ax1, ax2), (ax3, _)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Initial pH vs Total pH, pOH, and (pH + pOH) for Different Dilution Factors")

for df in dilution_factors:
    total_pH_values = []
    total_pOH_values = []
    total_sum_values = []

    for pH in initial_pH_values:
        diluted_pH, diluted_pOH = calculate_total_pH_pOH(pH, df)
        total_pH_values.append(diluted_pH)
        total_pOH_values.append(diluted_pOH)
        total_sum_values.append(diluted_pH + diluted_pOH)

    ax1.plot(initial_pH_values, total_pH_values, label=f'{df}x Dilution')
    ax2.plot(initial_pH_values, total_pOH_values, label=f'{df}x Dilution')

ax1.set_title("Initial pH vs Total pH")
ax1.set_xlabel("Initial pH")
ax1.set_ylabel("Total pH")
ax1.set_xlim(0, 14)
ax1.set_xticks(np.arange(0, 15, 1))
ax1.legend()
ax1.grid()

ax2.set_title("Initial pH vs Total pOH")
ax2.set_xlabel("Initial pH")
ax2.set_ylabel("Total pOH")
ax2.set_xlim(0, 14)
ax2.set_xticks(np.arange(0, 15, 1))
ax2.legend()
ax2.grid()

for df in dilution_factors:
    total_sum_values = [calculate_total_pH_pOH(pH, df)[0] + calculate_total_pH_pOH(pH, df)[1] for pH in initial_pH_values]
    ax3.plot(initial_pH_values, total_sum_values, label=f'{df}x Dilution')

ax3.axhline(y=14, color='red', linestyle='--', label="pH + pOH = 14")
ax3.set_title("Initial pH vs (pH + pOH)")
ax3.set_xlabel("Initial pH")
ax3.set_ylabel("pH + pOH")
ax3.set_xlim(0, 14)
ax3.set_xticks(np.arange(0, 15, 1))
ax3.legend()
ax3.grid()

fig.delaxes(_)
plt.tight_layout()
plt.show()