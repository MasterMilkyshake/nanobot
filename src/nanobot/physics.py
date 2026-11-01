"""Basic biophysics of a nanobot in blood and tumor vessels (SI units)."""

import numpy as np

K_B = 1.380649e-23  # Boltzmann constant, J/K
BODY_TEMP = 310.15  # K


def diffusivity(radius_m, viscosity_pa_s, temp_k=BODY_TEMP):
    """Stokes-Einstein diffusion coefficient (m^2/s)."""
    return K_B * temp_k / (6 * np.pi * viscosity_pa_s * radius_m)


def pore_hindrance(radius_m, pore_radius_m):
    """Renkin hindrance for a sphere diffusing through a cylindrical pore (0 to 1)."""
    lam = min(radius_m / pore_radius_m, 1.0)
    return (1 - lam) ** 2 * (1 - 2.104 * lam + 2.09 * lam**3 - 0.95 * lam**5)


def sieving(radius_m, pore_radius_m):
    """Renkin convective sieving coefficient, i.e. 1 - reflection coefficient (0 to 1)."""
    lam = min(radius_m / pore_radius_m, 1.0)
    phi = (1 - lam) ** 2
    return phi * (2 - phi) * (1 - 2 / 3 * lam**2 - 0.163 * lam**3)


def vessel_permeability(radius_m, pore_radius_m, porosity, wall_thickness_m, viscosity_pa_s):
    """Diffusive permeability of a leaky tumor vessel wall (m/s): P = porosity * H * D / L."""
    D = diffusivity(radius_m, viscosity_pa_s)
    return porosity * pore_hindrance(radius_m, pore_radius_m) * D / wall_thickness_m
