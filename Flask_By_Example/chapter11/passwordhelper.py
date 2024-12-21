import hashlib
import os
import base64

class PasswordHelper:

    def get_hash(self, plain_bytes):
        """
        Generate a SHA-512 hash for the given plain text.
        """
        if not isinstance(plain_bytes, bytes):
            raise TypeError("Input to get_hash must be bytes")
        return hashlib.sha512(plain_bytes).hexdigest()

    def get_salt(self):
        """
        Generate a random 20-byte salt encoded in base64.
        """
        return base64.b64encode(os.urandom(20)).decode('utf-8')  # Return salt as a string

    def validate_password(self, plain, salt, expected):
        """
        Validate the password by hashing the plain password with the salt and comparing with the expected hash.
        """
        # Ensure inputs are bytes
        if isinstance(plain, str):
            plain = plain.encode()  # Convert plain password to bytes
        if isinstance(salt, str):
            salt = salt.encode()  # Convert salt to bytes

        # Hash the combined plain text and salt
        return self.get_hash(plain + salt) == expected
