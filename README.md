# nanobot

A small computational model of a therapeutic nanobot (nanocarrier). It predicts
where an IV dose goes (plasma, liver/spleen, tumor, urine) based on the bot's
design. Built as a starting point for work aligned with the Dogra Lab (USC Mann
School of Pharmacy), which uses mechanistic modeling to predict how nanomedicines
are distributed in the body and delivered to tumors.

## Layout

```
src/nanobot/
  design.py    # Nanobot: design parameters (size, stealth coating)
  physics.py   # equations that set the rates (diffusion, pore hindrance, permeability)
  model.py     # 4-compartment ODE model + simulate()
examples/size_sweep.py
tests/test_model.py
```

## Model

Amounts are in % injected dose (%ID); time is in hours.

- **Kidney clearance:** GFR × Renkin sieving through a ~4.5 nm glomerular pore.
- **Liver/spleen (MPS) uptake:** scales with size and surface (stealth) recognition.
- **Tumor uptake:** pore-theory permeability `P = porosity · H(r/r_pore) · D / L_wall`.
  `D` is the Stokes–Einstein diffusivity. Tumor values are from Dogra et al. 2020.

The parameter values are illustrative and not fitted to data.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python examples/size_sweep.py
.venv/bin/python -m pytest
```

## Reference

Dogra P, et al. *A mathematical model to predict nanomedicine pharmacokinetics and
tumor delivery.* Comput Struct Biotechnol J. 2020;18:518–531.
