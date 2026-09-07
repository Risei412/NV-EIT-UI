"""Parameter JSON in, spectrum + window JSON out."""
from __future__ import annotations

from .lambda_system import chi_cut, chi_probe, transmission_from_chi
from .windows import window_features
import numpy as np

PRESETS = {
    "lambda": {
        "preset": "lambda",
        "omega_c": 0.8,
        "gamma_e": 1.0,
        "gamma_g": 0.0,
        "delta_c": 0.0,
        "optical_depth": 3.0,
        "delta_min": -5.0,
        "delta_max": 5.0,
        "n_points": 401,
    }
}


def compute_transmission(params: dict | None = None) -> dict:
    p = dict(PRESETS["lambda"])
    if params:
        preset = params.get("preset", "lambda")
        if preset in PRESETS:
            p.update(PRESETS[preset])
        p.update({k: v for k, v in params.items() if v is not None})

    n = int(p["n_points"])
    if n < 51 or n > 2001:
        raise ValueError("n_points must be in [51, 2001]")

    det = np.linspace(float(p["delta_min"]), float(p["delta_max"]), n)
    chi_f = chi_probe(det, float(p["omega_c"]), float(p["gamma_e"]), float(p["gamma_g"]), float(p["delta_c"]))
    chi_c = chi_cut(det, float(p["gamma_e"]))
    im_ref = float(np.imag(chi_cut(np.array([0.0]), float(p["gamma_e"])))[0])
    if im_ref <= 0:
        im_ref = 1.0

    t_f = transmission_from_chi(chi_f, float(p["optical_depth"]), im_ref)
    t_c = transmission_from_chi(chi_c, float(p["optical_depth"]), im_ref)

    window = window_features(det, t_f, t_c, np.imag(chi_f), np.imag(chi_c))
    return {
        "params": {
            "preset": p.get("preset", "lambda"),
            "omega_c": float(p["omega_c"]),
            "gamma_e": float(p["gamma_e"]),
            "gamma_g": float(p["gamma_g"]),
            "delta_c": float(p["delta_c"]),
            "optical_depth": float(p["optical_depth"]),
        },
        "spectrum": {
            "detuning": det.tolist(),
            "T_full": t_f.tolist(),
            "T_cut": t_c.tolist(),
            "im_chi_full": np.imag(chi_f).tolist(),
            "im_chi_cut": np.imag(chi_c).tolist(),
        },
        "window": window,
        "note": "Textbook Lambda linear response. Not an NV exponent certificate.",
    }
