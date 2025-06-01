import hmac
import hashlib
import os

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

def verify_signature(request_body: bytes, signature: str) -> bool:
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=request_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)
