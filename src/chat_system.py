from .user import User
from .message import SecureMessage

class SecureChatSystem:
    """
    Main application class managing users and messages.
    
    Provides:
    - User registration and authentication
    - Secure message sending and receiving
    - Key management
    """
    
    def __init__(self):
        """Initialize empty chat system."""
        self.users = {}  # username -> User object
        self.messages = []  # List of SecureMessage objects
    
    def register_user(self, username, password):
        """
        Register a new user.
        
        Args:
            username (str): Desired username
            password (str): User password
            
        Returns:
            bool: True if registration successful
            
        Raises:
            ValueError: If username already exists
        """
        if username in self.users:
            raise ValueError(f"Username '{username}' already exists")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        self.users[username] = User(username, password)
        print(f"✅ User '{username}' registered successfully")
        print(f"   🔑 RSA keys generated (2048-bit)")
        print(f"   🔑 ECDH keys generated (256-bit)")
        print(f"   🔑 ECDSA keys generated (256-bit)")
        return True
    
    def authenticate_user(self, username, password):
        """
        Authenticate user login.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if authentication successful
        """
        if username not in self.users:
            return False
        
        return self.users[username].authenticate(password)
    
    def send_message(self, sender_username, recipient_username, message):
        """
        Send encrypted message between users.
        
        Args:
            sender_username (str): Sender's username
            recipient_username (str): Recipient's username
            message (str): Message content
            
        Returns:
            SecureMessage: The encrypted message object
            
        Raises:
            ValueError: If users don't exist
        """
        if sender_username not in self.users:
            raise ValueError(f"Sender '{sender_username}' not found")
        if recipient_username not in self.users:
            raise ValueError(f"Recipient '{recipient_username}' not found")
        
        sender = self.users[sender_username]
        recipient = self.users[recipient_username]
        
        # Create encrypted message
        secure_msg = SecureMessage(
            sender_username,
            recipient_username,
            message,
            sender.ecdh_private,
            recipient.ecdh_public,
            sender.ecdsa_private
        )
        
        self.messages.append(secure_msg)
        
        print(f"\n📤 Message sent from {sender_username} to {recipient_username}")
        print(f"   🔒 Encrypted with AES-256-GCM")
        print(f"   🔑 Key exchanged via ECDH")
        print(f"   ✍️  Signed with ECDSA")
        print(f"   🛡️  Protected with HMAC-SHA256")
        
        return secure_msg
    
    def get_messages_for_user(self, username):
        """
        Get all messages sent to a user.
        
        Args:
            username (str): Username
            
        Returns:
            list: Messages addressed to the user
        """
        return [msg for msg in self.messages if msg.recipient == username]
    
    def read_message(self, message, recipient_username):
        """
        Decrypt and read a message.
        
        Args:
            message (SecureMessage): Message to read
            recipient_username (str): Recipient's username
            
        Returns:
            tuple: (plaintext, is_verified)
        """
        if recipient_username not in self.users:
            raise ValueError(f"User '{recipient_username}' not found")
        
        recipient = self.users[recipient_username]
        sender = self.users[message.sender]
        
        plaintext, is_verified = message.decrypt(
            recipient.ecdh_private,
            sender.ecdh_public,
            sender.ecdsa_public
        )
        
        verification_status = "✅ VERIFIED" if is_verified else "❌ UNVERIFIED"
        print(f"\n📨 Message from {message.sender}:")
        print(f"   Content: {plaintext}")
        print(f"   Signature: {verification_status}")
        print(f"   Time: {message.timestamp}")
        
        return plaintext, is_verified

