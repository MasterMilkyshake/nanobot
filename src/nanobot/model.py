"""Minimal whole-body model: plasma, MPS (liver/spleen), tumor, urine.

Amounts are in % injected dose (%ID); time is in hours. Rates come from
biophysics (see physics.py), loosely following Dogra et al., CSBJ 2020.
"""

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from . import physics
from .design import Nanobot

COMPARTMENTS = ("plasma", "mps", "tumor", "urine")


@dataclass
class Body:
    """Mouse-scale defaults. Tumor values from Dogra et al. 2020."""

    plasma_volume_ml: float = 1.0
    gfr_ml_h: float = 15.0
    glomerular_pore_nm: float = 4.5
    mps_rate_100nm_per_h: float = 1.0  # MPS uptake rate for a bare 100 nm particle

    tumor_volume_ml: float = 0.5
    tumor_interstitial_fraction: float = 0.4
    tumor_vessel_surface_per_m: float = 4e4  # 40 mm^2/mm^3
    tumor_pore_nm: float = 850.0
    tumor_porosity: float = 1e-3
    tumor_wall_thickness_m: float = 5e-6
    tumor_blood_viscosity_pa_s: float = 7.42e-3


def rates(bot: Nanobot, body: Body) -> dict[str, float]:
    """First-order rate constants (1/h) for the nanobot in this body."""
    r = bot.radius_m

    renal = body.gfr_ml_h * physics.sieving(r, body.glomerular_pore_nm * 1e-9) / body.plasma_volume_ml
    mps = body.mps_rate_100nm_per_h * bot.mps_recognition * (bot.diameter_nm / 100.0)

    P = physics.vessel_permeability(
        r, body.tumor_pore_nm * 1e-9, body.tumor_porosity,
        body.tumor_wall_thickness_m, body.tumor_blood_viscosity_pa_s,
    )
    PS_ml_h = P * body.tumor_vessel_surface_per_m * body.tumor_volume_ml * 3600
    tumor_in = PS_ml_h / body.plasma_volume_ml
    tumor_out = PS_ml_h / (body.tumor_interstitial_fraction * body.tumor_volume_ml)

    return {"renal": renal, "mps": mps, "tumor_in": tumor_in, "tumor_out": tumor_out}


def simulate(bot: Nanobot, body: Body | None = None, hours: float = 72.0, dt: float = 0.25) -> dict[str, np.ndarray]:
    """Simulate one IV bolus (100 %ID into plasma). Returns time plus %ID per compartment."""
    body = body or Body()
    k = rates(bot, body)

    def rhs(t, y):
        plasma, mps, tumor, urine = y
        return [
            -(k["renal"] + k["mps"] + k["tumor_in"]) * plasma + k["tumor_out"] * tumor,
            k["mps"] * plasma,
            k["tumor_in"] * plasma - k["tumor_out"] * tumor,
            k["renal"] * plasma,
        ]

    t = np.arange(0.0, hours + dt / 2, dt)
    sol = solve_ivp(rhs, (0.0, hours), [100.0, 0.0, 0.0, 0.0], t_eval=t, method="LSODA", rtol=1e-8, atol=1e-10)
    return {"t": sol.t, **dict(zip(COMPARTMENTS, sol.y))}
