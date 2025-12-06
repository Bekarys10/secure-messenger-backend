from .crypto_engine import CryptoEngine

class User:
    """
    Represents a user in the SecureChat system.
    
    Each user has:
    - Username and password hash
    - RSA key pair for key encryption
    - ECDH key pair for key exchange
    - ECDSA key pair for signatures
    """
    
    def __init__(self, username, password):
        """
        Initialize new user with cryptographic keys.
        
        Args:
            username (str): User's username
            password (str): User's password (will be hashed)
        """
        self.username = username
        self.password_hash = CryptoEngine.hash_password(password)
        
        # Generate all required key pairs
        self.rsa_private, self.rsa_public = CryptoEngine.generate_rsa_keypair()
        self.ecdh_private, self.ecdh_public = CryptoEngine.generate_ecdh_keypair()
        self.ecdsa_private, self.ecdsa_public = CryptoEngine.generate_ecdh_keypair()
    
    def authenticate(self, password):
        """
        Verify user's password.
        
        Args:
            password (str): Password to verify
            
        Returns:
            bool: True if password is correct
        """
        return CryptoEngine.verify_password(password, self.password_hash)

