import numpy as np

from nanobot import Nanobot, simulate


def test_mass_is_conserved():
    out = simulate(Nanobot(diameter_nm=50))
    total = out["plasma"] + out["mps"] + out["tumor"] + out["urine"]
    assert np.allclose(total, 100.0, atol=1e-6)


def test_small_bots_are_cleared_by_kidney_large_are_not():
    assert simulate(Nanobot(diameter_nm=4))["urine"][-1] > 50
    assert simulate(Nanobot(diameter_nm=100))["urine"][-1] < 1e-6


def test_stealth_coating_reduces_mps_uptake():
    bare = simulate(Nanobot(diameter_nm=100, mps_recognition=1.0))["mps"][-1]
    stealth = simulate(Nanobot(diameter_nm=100, mps_recognition=0.1))["mps"][-1]
    assert stealth < bare
