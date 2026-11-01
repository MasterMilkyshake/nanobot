"""How nanobot size changes where the dose goes (single IV dose, 72 h)."""

from nanobot import Nanobot, simulate

print(f"{'diameter (nm)':>14} {'tumor peak %ID':>15} {'MPS %ID':>9} {'urine %ID':>10}")
for d in [5, 10, 20, 50, 100, 200]:
    out = simulate(Nanobot(diameter_nm=d))
    print(f"{d:>14} {out['tumor'].max():>15.2f} {out['mps'][-1]:>9.1f} {out['urine'][-1]:>10.1f}")
