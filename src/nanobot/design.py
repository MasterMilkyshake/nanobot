"""Nanobot design parameters."""

from dataclasses import dataclass


@dataclass
class Nanobot:
    diameter_nm: float = 100.0  # hydrodynamic diameter
    mps_recognition: float = 1.0  # 1 = bare surface, < 1 = stealth coating (e.g. PEG)

    @property
    def radius_m(self) -> float:
        return self.diameter_nm * 1e-9 / 2
