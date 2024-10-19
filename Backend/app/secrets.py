import secrets

def genrate_secret_key():
    secret_key = secrets.token_hex(32)  # Generates a 64-character (256-bit) secret key
    return secret_key