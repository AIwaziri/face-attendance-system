from auth import hash_password, verify_password, create_access_token

password = "1234567890"

hashed = hash_password(password)
print("HASH OK")

assert verify_password(password, hashed)
print("VERIFY OK")

token = create_access_token({"sub": "user123"})
print("JWT OK:", token[:30])