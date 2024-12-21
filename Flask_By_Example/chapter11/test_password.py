from passwordhelper import PasswordHelper
ph = PasswordHelper()

# Generate a salt
salt = ph.get_salt()
print("Generated Salt:", salt)

# Hash a password with the salt
password = "my_secure_password"
hashed_password = ph.get_hash((password + salt).encode())
print("Hashed Password:", hashed_password)

# Validate the password
is_valid = ph.validate_password(password, salt, hashed_password)
print("Password is valid:", is_valid)

# Test with an incorrect password
is_valid_wrong = ph.validate_password("wrong_password", salt, hashed_password)
print("Password is valid (wrong):", is_valid_wrong)
