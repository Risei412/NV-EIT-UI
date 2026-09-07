"""Textbook 3-level Lambda linear probe response.

Extracted conceptually from Risei412/NV-EIT-space Lambda-chain machinery,
but this file is self-contained and has no file I/O.
"""
from __future__ import annotations

import numpy as np


def chi_probe(delta, omega_c, gamma_e, gamma_g, delta_c=0.0):
    """Complex probe susceptibility (arbitrary units).

    chi = (gamma_g - i (delta - delta_c))
          / [(gamma_e - i delta)(gamma_g - i (delta - delta_c)) + Omega_c^2 / 4]
    """
    d = np.asarray(delta, dtype=float)
    num = gamma_g - 1j * (d - delta_c)
    den = (gamma_e - 1j * d) * (gamma_g - 1j * (d - delta_c)) + (omega_c ** 2) / 4.0
    return num / den


def chi_cut(delta, gamma_e):
    """Control-off (sector-cut) probe response."""
    d = np.asarray(delta, dtype=float)
    return 1.0 / (gamma_e - 1j * d)


def transmission_from_chi(chi, optical_depth, im_ref):
    """Thin-sample-style transmission from Im chi.

    T = exp(-OD * Im(chi) / Im_ref), with Im_ref = Im chi_cut(0) > 0.
    """
    ratio = np.clip(np.real(chi) * 0 + np.imag(chi) / im_ref, 0.0, None)
    return np.exp(-optical_depth * ratio)
