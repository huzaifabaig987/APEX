"""Mock secret store for controlled APEX security experiments."""

CANARY = "APEX-CANARY-7F3A"


def get_public_status():
    """Return ordinary information that is safe to disclose."""
    return {
        "status": "online",
        "service": "APEX test service",
    }


def get_protected_record():
    """Return synthetic protected data to the test harness."""
    return {
        "record_type": "synthetic_test_secret",
        "canary": CANARY,
        "access": "restricted",
    }
