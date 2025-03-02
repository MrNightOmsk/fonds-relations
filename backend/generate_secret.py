import secrets

secret_key = secrets.token_urlsafe(32)
print(f"\nВаш APP_SECRET_KEY:\n{secret_key}\n") 