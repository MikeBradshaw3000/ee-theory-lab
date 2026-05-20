import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# OLS Empirical Coefficients from your Tier 3 Report
b_0 = -0.9721
b_L = 1.0274
b_D = 0.6582
b_LD = 0.0710

# Generate grid space over the observed empirical ranges
drive_range = np.linspace(-3.0, 1.0, 500)
lambda_levels = [0.1, 0.5, 0.9]  # Low, Mid, High structural conduciveness
colors = ['#e74c3c', '#f39c12', '#2ecc71']

plt.figure(figsize=(10, 6), dpi=300)

for L, color in zip(lambda_levels, colors):
    # Calculate logit space
    logit_p = b_0 + (b_L * L) + (b_D * drive_range) + (b_LD * (L * drive_range))
    # Invert logit to raw probability space to visualize the phase transition curve
    p_act = 1 / (1 + np.exp(-logit_p))
    
    plt.plot(drive_range, p_act, label=f'Lambda_total = {L} (Conduciveness)', color=color, lw=2.5)

# Highlighting the sharp bifurcation region
plt.axvspan(-2.0, -1.0, color='gray', alpha=0.15, label='Empirical Stabilization Corridor')

plt.title('Phase 4B Cascade Bifurcation: Interaction of Conduciveness & Drive', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Thermodynamic Drive Energy (Drive_Raw)', fontsize=10)
plt.ylabel('Probability of State Activation (p_act)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none')
plt.tight_layout()

out_path = Path("tier3_outputs/bifurcation_threshold.png")
out_path.parent.mkdir(exist_ok=True)
plt.savefig(out_path)
print(f"[SUCCESS] Bifurcation plot saved directly to: {out_path}")