"""
Cryptographic Engine Module
Implements all cryptographic operations for SecureChat.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import bcrypt
import os
import base64


class CryptoEngine:
    """Core cryptographic operations."""
    
    @staticmethod
    def generate_rsa_keypair():
        """Generate RSA-2048 key pair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key, private_key.public_key()
    
    @staticmethod
    def generate_ecdh_keypair():
        """Generate ECDH key pair using SECP256R1 curve."""
        private_key = ec.generate_private_key(
            ec.SECP256R1(),
            default_backend()
        )
        return private_key, private_key.public_key()
    
    @staticmethod
    def derive_shared_secret(private_key, peer_public_key):
        """Derive shared secret using ECDH."""
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        
        # Derive proper encryption key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'SecureChat ECDH',
            backend=default_backend()
        ).derive(shared_key)
        
        return derived_key
    
    @staticmethod
    def aes_encrypt(plaintext, key):
        """Encrypt using AES-256-GCM."""
        nonce = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'nonce': base64.b64encode(nonce).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }
    
    @staticmethod
    def aes_decrypt(encrypted_data, key):
        """Decrypt using AES-256-GCM."""
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        nonce = base64.b64decode(encrypted_data['nonce'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        return plaintext.decode()
    
    @staticmethod
    def sign_message(message, private_key):
        """Create ECDSA signature."""
        signature = private_key.sign(
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode()
    
    @staticmethod
    def verify_signature(message, signature, public_key):
        """Verify ECDSA signature."""
        try:
            public_key.verify(
                base64.b64decode(signature),
                message.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False
    
    @staticmethod
    def generate_hmac(message, key):
        """Generate HMAC-SHA256."""
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(message.encode())
        return base64.b64encode(h.finalize()).decode()
    
    @staticmethod
    def verify_hmac(message, hmac_value, key):
        """Verify HMAC-SHA256."""
        try:
            h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
            h.update(message.encode())
            h.verify(base64.b64decode(hmac_value))
            return True
        except:
            return False
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt)
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against bcrypt hash."""
        try:
            return bcrypt.checkpw(password.encode(), hashed)
        except:
            return False

