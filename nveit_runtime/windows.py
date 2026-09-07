"""EIT-window scalars from a transmission curve."""
from __future__ import annotations

import numpy as np


def window_features(detuning, t_full, t_cut, im_chi_full, im_chi_cut):
    detuning = np.asarray(detuning, dtype=float)
    t_full = np.asarray(t_full, dtype=float)
    t_cut = np.asarray(t_cut, dtype=float)
    im_full = np.asarray(im_chi_full, dtype=float)
    im_cut = np.asarray(im_chi_cut, dtype=float)

    i0 = int(np.argmax(t_full))
    center = float(detuning[i0])
    t_peak = float(t_full[i0])
    t_off = float(t_cut[i0]) if t_cut.size == t_full.size else float(min(t_full[0], t_full[-1]))
    depth = float(t_peak - t_off)

    half = t_off + 0.5 * depth
    fwhm = _fwhm(detuning, t_full, half, i0) if depth > 1e-12 else None

    a_full = float(im_full[i0])
    a_cut = float(im_cut[i0]) if im_cut.size == im_full.size else float(np.max(im_cut))
    delta_a = float(a_cut - a_full)
    c_max = float(delta_a / a_cut) if abs(a_cut) > 1e-18 else None

    if depth >= 0.25 and fwhm is not None:
        verdict = "WINDOW_PRESENT"
    elif depth >= 0.02 or (c_max is not None and c_max >= 1e-4):
        verdict = "SHALLOW"
    else:
        verdict = "ABSENT"

    return {
        "center_detuning": center,
        "fwhm": fwhm,
        "depth": depth,
        "T_min_absorption_peak_proxy": float(np.min(t_full)),
        "T_at_window": t_peak,
        "T_off": t_off,
        "C_max": c_max,
        "delta_A_at_peak": delta_a,
        "verdict": verdict,
    }


def _fwhm(x, y, half, ipeak):
    left = None
    for i in range(ipeak, 0, -1):
        if y[i] <= half:
            left = float(np.interp(half, [y[i], y[i + 1]], [x[i], x[i + 1]]))
            break
    right = None
    for i in range(ipeak, len(y) - 1):
        if y[i] <= half:
            right = float(np.interp(half, [y[i], y[i - 1]], [x[i], x[i - 1]]))
            break
    if left is None or right is None:
        return None
    return float(right - left)
