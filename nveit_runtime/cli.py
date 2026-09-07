from __future__ import annotations

import argparse
import json

from .api import compute_transmission


def main():
    parser = argparse.ArgumentParser(description="NV-EIT-UI local spectrum")
    parser.add_argument("--preset", default="lambda")
    parser.add_argument("--omega-c", type=float, default=None)
    parser.add_argument("--gamma-g", type=float, default=None)
    args = parser.parse_args()
    params = {"preset": args.preset}
    if args.omega_c is not None:
        params["omega_c"] = args.omega_c
    if args.gamma_g is not None:
        params["gamma_g"] = args.gamma_g
    out = compute_transmission(params)
    slim = {"params": out["params"], "window": out["window"], "n": len(out["spectrum"]["detuning"])}
    print(json.dumps(slim, indent=2))


if __name__ == "__main__":
    main()
