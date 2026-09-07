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
apps/api/          Lambda handler + local server
apps/web/          static UI
infra/             SAM template
```

## Local

```bash
pip install -r requirements.txt
python -m nveit_runtime.cli --preset lambda
python apps/api/local_server.py   # http://127.0.0.1:8080
```

## Lambda (ap-northeast-1)

Needs AWS CLI + [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html), and an IAM user/role that can deploy CloudFormation.

```bash
aws configure   # region: ap-northeast-1
cd infra
sam build
sam deploy
```

Deploy output includes `SpectrumApi`, for example:

```
https://xxxx.execute-api.ap-northeast-1.amazonaws.com/spectrum
```

Check:

```bash
curl -s -X POST "$SPECTRUM_API" \
  -H 'content-type: application/json' \
  -d '{"preset":"lambda","omega_c":0.8,"gamma_g":0}'
```

Then open `apps/web/index.html` and set **API URL** to that endpoint (saved in the browser). Local server still uses `/spectrum` on the same origin.

First invoke may take a few seconds (cold start + numpy).
