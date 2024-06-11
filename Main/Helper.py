import hashlib

def mask_data(value: str) -> str:
    #Convert sensitive data into a SHA-256 hash for privacy.
    return hashlib.sha256(value.encode()).hexdigest()
