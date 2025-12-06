import json
from datetime import datetime
from .crypto_engine import CryptoEngine

class SecureMessage:
    """
    Represents an encrypted message with all security metadata.
    
    Contains:
    - Encrypted content
    - Digital signature
    - HMAC for integrity
    - Timestamp
    """
    
    def __init__(self, sender, recipient, plaintext, sender_ecdh_private, 
                 recipient_ecdh_public, sender_ecdsa_private):
        """
        Create and encrypt a new secure message.
        
        Args:
            sender (str): Sender username
            recipient (str): Recipient username
            plaintext (str): Message content
            sender_ecdh_private: Sender's ECDH private key
            recipient_ecdh_public: Recipient's ECDH public key
            sender_ecdsa_private: Sender's ECDSA private key
        """
        self.sender = sender
        self.recipient = recipient
        self.timestamp = datetime.now().isoformat()
        
        # Derive shared secret using ECDH
        self.shared_secret = CryptoEngine.derive_shared_secret(
            sender_ecdh_private,
            recipient_ecdh_public
        )
        
        # Encrypt message with AES-256-GCM
        self.encrypted_data = CryptoEngine.aes_encrypt(plaintext, self.shared_secret)
        
        # Sign the plaintext message
        self.signature = CryptoEngine.sign_message(plaintext, sender_ecdsa_private)
        
        # Generate HMAC for integrity
        message_for_hmac = json.dumps(self.encrypted_data)
        self.hmac = CryptoEngine.generate_hmac(message_for_hmac, self.shared_secret)
    
    def decrypt(self, recipient_ecdh_private, sender_ecdh_public, sender_ecdsa_public):
        """
        Decrypt and verify message.
        
        Args:
            recipient_ecdh_private: Recipient's ECDH private key
            sender_ecdh_public: Sender's ECDH public key
            sender_ecdsa_public: Sender's ECDSA public key
            
        Returns:
            tuple: (decrypted_message, is_verified)
        """
        # Derive same shared secret
        shared_secret = CryptoEngine.derive_shared_secret(
            recipient_ecdh_private,
            sender_ecdh_public
        )
        
        # Verify HMAC
        message_for_hmac = json.dumps(self.encrypted_data)
        if not CryptoEngine.verify_hmac(message_for_hmac, self.hmac, shared_secret):
            raise ValueError("HMAC verification failed - message may be tampered")
        
        # Decrypt message
        plaintext = CryptoEngine.aes_decrypt(self.encrypted_data, shared_secret)
        
        # Verify signature
        is_verified = CryptoEngine.verify_signature(
            plaintext,
            self.signature,
            sender_ecdsa_public
        )
        
        return plaintext, is_verified
    
    def to_dict(self):
        """
        Convert message to dictionary for storage/transmission.
        
        Returns:
            dict: Serializable message data
        """
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
            'encrypted_data': self.encrypted_data,
            'signature': self.signature,
            'hmac': self.hmac
        }

