import hashlib
import base64
import os
from itertools import cycle

class MessageEncryption:
    def __init__(self):
        self.key = None

    def generate_key(self, password):
        """Generate encryption key from password"""
        # Create a strong key using SHA-256
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt_message(self, message):
        """Encrypt a message using XOR with the key"""
        if not self.key:
            raise ValueError("Key not generated. Call generate_key first.")
        
        # Convert message to bytes if it's a string
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # XOR the message with the key
        encrypted = bytes(a ^ b for a, b in zip(message, cycle(self.key)))
        
        # Convert to base64 for safe transmission
        return base64.b64encode(encrypted)

    def decrypt_message(self, encrypted_message):
        """Decrypt a message"""
        if not self.key:
            raise ValueError("Key not generated. Call generate_key first.")
        
        # Decode from base64
        encrypted = base64.b64decode(encrypted_message)
        
        # XOR with the key to decrypt
        decrypted = bytes(a ^ b for a, b in zip(encrypted, cycle(self.key)))
        
        # Try to decode as UTF-8, return bytes if it fails
        try:
            return decrypted.decode('utf-8')
        except UnicodeDecodeError:
            return decrypted

    def encrypt_file(self, file_path):
        """Encrypt a file"""
        if not self.key:
            raise ValueError("Key not generated. Call generate_key first.")
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = self.encrypt_message(file_data)
        
        # Save encrypted file
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        
        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        """Decrypt a file"""
        if not self.key:
            raise ValueError("Key not generated. Call generate_key first.")
        
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = self.decrypt_message(encrypted_data)
        
        # Save decrypted file
        decrypted_file_path = encrypted_file_path.replace('.encrypted', '.decrypted')
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data.encode())
        
        return decrypted_file_path 