# NV-EIT-UI

Independent UI + API for NV-EIT transmission spectra.
Claims and gate certificates stay in [NV-EIT-space](https://github.com/Risei412/NV-EIT-space).

This repo returns:

- transmission spectrum \(T(\delta)\) and \(\mathrm{Im}\,\chi(\delta)\)
- EIT-window features (center, FWHM, depth, contrast, verdict)

It does **not** claim unconstrained exponent identification.

## Layout

```
nveit_runtime/     pure functions (no file I/O)
apps/api/          Lambda handler
apps/web/          static UI
infra/             SAM template
```

## Local

```bash
pip install -r requirements.txt
python -m nveit_runtime.cli --preset lambda
python apps/api/local_server.py   # http://127.0.0.1:8080
```

Open `apps/web/index.html` (set `API_URL` to the local server or a Function URL).

## Lambda (later)

Container image from `apps/api/Dockerfile`. POST `/spectrum` with the JSON body documented in `nveit_runtime/api.py`.
