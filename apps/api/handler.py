from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nveit_runtime.api import compute_transmission

CORS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Methods": "OPTIONS,POST",
}


def lambda_handler(event, context):
    method = (
        (event.get("requestContext") or {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or "POST"
    )
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS, "body": ""}

    raw = event.get("body") if isinstance(event, dict) else None
    if raw is None:
        params = event if isinstance(event, dict) else {}
    elif isinstance(raw, str):
        params = json.loads(raw) if raw else {}
    else:
        params = raw

    try:
        result = compute_transmission(params or {})
        return {"statusCode": 200, "headers": CORS, "body": json.dumps(result)}
    except ValueError as exc:
        return {"statusCode": 400, "headers": CORS, "body": json.dumps({"error": str(exc)})}
    except Exception as exc:
        return {"statusCode": 500, "headers": CORS, "body": json.dumps({"error": type(exc).__name__})}
