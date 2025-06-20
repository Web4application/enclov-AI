import hmac
import hashlib

GITHUB_SECRET = b'your_github_webhook_secret_here'

def verify_signature(body: bytes, signature: str) -> bool:
    if not signature:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_SECRET, msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)
