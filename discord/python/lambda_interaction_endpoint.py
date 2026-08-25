"""
AWS Lambda handler for a Discord Interactions endpoint.
Designed for use behind a Lambda Function URL (no API Gateway needed).

Handles:
  - PING (type 1) -> PONG
  - APPLICATION_COMMAND (type 2) -> /start

Env vars required:
  DISCORD_PUBLIC_KEY  - from your Discord app's "General Information" page

Dependencies (bundle into your deployment package / layer):
  PyNaCl
"""

import json
import os
import boto3

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]

# Discord interaction type constants
TYPE_PING = 1
TYPE_APPLICATION_COMMAND = 2

# Discord response type constants
PONG = 1
CHANNEL_MESSAGE_WITH_SOURCE = 4

lambda_client = boto3.client('lambda')

def verify_signature(public_key: str, signature: str, timestamp: str, body: str) -> bool:
    verify_key = VerifyKey(bytes.fromhex(public_key))
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except (BadSignatureError, ValueError):
        return False


def _response(status_code: int, body: dict | None = None) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body) if body is not None else "",
    }


def lambda_handler(event, context):
    # Lambda Function URL puts headers here; keys arrive lowercased.
    headers = event.get("headers") or {}
    signature = headers.get("x-signature-ed25519")
    timestamp = headers.get("x-signature-timestamp")
    raw_body = event.get("body") or ""

    if event.get("isBase64Encoded"):
        import base64
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    if not signature or not timestamp:
        return _response(401, {"error": "missing signature headers"})

    if not verify_signature(DISCORD_PUBLIC_KEY, signature, timestamp, raw_body):
        return _response(401, {"error": "invalid request signature"})

    interaction = json.loads(raw_body)
    interaction_type = interaction.get("type")

    if interaction_type == TYPE_PING:
        return _response(200, {"type": PONG})

    if interaction_type == TYPE_APPLICATION_COMMAND:
        command_name = interaction.get("data", {}).get("name")

        if command_name == "<CMD>":
            pass
            # return _response(200, handle_start_command(interaction))

        return _response(
            200,
            {
                "type": CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {"content": f"Unknown command: {command_name}"},
            },
        )

    return _response(400, {"error": "unhandled interaction type"})