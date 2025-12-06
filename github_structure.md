# Complete GitHub Repository Structure & Files

## 📁 Repository Structure

```
securechat/
│
├── README.md                          # Main project documentation
├── LICENSE                            # MIT License
├── .gitignore                        # Git ignore file
├── requirements.txt                   # Python dependencies
│
├── src/                              # Source code directory
│   ├── __init__.py
│   ├── main.py                       # Main application entry point
│   ├── crypto_engine.py              # Cryptographic operations
│   ├── user.py                       # User class
│   ├── message.py                    # Message class
│   ├── chat_system.py                # Main system logic
│   │
│   ├── web/                          # Web interface (React)
│   │   ├── package.json
│   │   ├── public/
│   │   │   └── index.html
│   │   └── src/
│   │       ├── App.jsx               # Main React component
│   │       ├── components/
│   │       │   ├── Login.jsx
│   │       │   ├── Register.jsx
│   │       │   ├── ChatInterface.jsx
│   │       │   └── MessageList.jsx
│   │       └── utils/
│   │           └── crypto.js         # Crypto utilities
│   │
│   └── tests/                        # Unit tests
│       ├── __init__.py
│       ├── test_crypto.py
│       ├── test_user.py
│       └── test_message.py
│
├── docs/                             # Documentation
│   ├── architecture.md               # System architecture
│   ├── security.md                   # Security analysis
│   ├── api.md                        # API documentation
│   ├── user_guide.md                 # User manual
│   └── presentation/
│       ├── presentation.md           # Presentation guide
│       └── slides.pdf                # Presentation slides
│
├── examples/                         # Usage examples
│   ├── basic_usage.py
│   ├── advanced_features.py
│   └── demo.py
│
└── assets/                           # Images and diagrams
    ├── architecture_diagram.png
    ├── encryption_flow.png
    └── logo.png
```

---

## 📄 File Contents

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db

# Node (for React frontend)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local

# Database (if added later)
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
```

---

### LICENSE (MIT)

```text
MIT License

Copyright (c) 2024 Bekarys, Aslan, Bekbol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### src/crypto_engine.py

```python
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
```

---

### src/tests/test_crypto.py

```python
"""
Unit tests for cryptographic operations.
"""

import pytest
from src.crypto_engine import CryptoEngine
import os


class TestCryptoEngine:
    """Test suite for CryptoEngine."""
    
    def test_rsa_key_generation(self):
        """Test RSA key pair generation."""
        private, public = CryptoEngine.generate_rsa_keypair()
        assert private is not None
        assert public is not None
    
    def test_ecdh_key_generation(self):
        """Test ECDH key pair generation."""
        private, public = CryptoEngine.generate_ecdh_keypair()
        assert private is not None
        assert public is not None
    
    def test_ecdh_key_exchange(self):
        """Test ECDH shared secret derivation."""
        # Generate two key pairs
        alice_private, alice_public = CryptoEngine.generate_ecdh_keypair()
        bob_private, bob_public = CryptoEngine.generate_ecdh_keypair()
        
        # Derive shared secrets
        alice_secret = CryptoEngine.derive_shared_secret(alice_private, bob_public)
        bob_secret = CryptoEngine.derive_shared_secret(bob_private, alice_public)
        
        # Both should derive the same secret
        assert alice_secret == bob_secret
        assert len(alice_secret) == 32
    
    def test_aes_encryption_decryption(self):
        """Test AES-256-GCM encryption and decryption."""
        key = os.urandom(32)
        plaintext = "This is a secret message"
        
        # Encrypt
        encrypted = CryptoEngine.aes_encrypt(plaintext, key)
        assert 'ciphertext' in encrypted
        assert 'nonce' in encrypted
        assert 'tag' in encrypted
        
        # Decrypt
        decrypted = CryptoEngine.aes_decrypt(encrypted, key)
        assert decrypted == plaintext
    
    def test_aes_wrong_key(self):
        """Test that wrong key fails decryption."""
        key1 = os.urandom(32)
        key2 = os.urandom(32)
        plaintext = "Secret message"
        
        encrypted = CryptoEngine.aes_encrypt(plaintext, key1)
        
        with pytest.raises(Exception):
            CryptoEngine.aes_decrypt(encrypted, key2)
    
    def test_digital_signature(self):
        """Test ECDSA signature creation and verification."""
        private, public = CryptoEngine.generate_ecdh_keypair()
        message = "Test message"
        
        # Sign
        signature = CryptoEngine.sign_message(message, private)
        assert signature is not None
        
        # Verify
        is_valid = CryptoEngine.verify_signature(message, signature, public)
        assert is_valid is True
    
    def test_signature_tampering(self):
        """Test that tampered message fails verification."""
        private, public = CryptoEngine.generate_ecdh_keypair()
        message = "Original message"
        tampered_message = "Tampered message"
        
        signature = CryptoEngine.sign_message(message, private)
        is_valid = CryptoEngine.verify_signature(tampered_message, signature, public)
        
        assert is_valid is False
    
    def test_hmac_generation_verification(self):
        """Test HMAC generation and verification."""
        key = os.urandom(32)
        message = "Test message"
        
        # Generate HMAC
        hmac_value = CryptoEngine.generate_hmac(message, key)
        assert hmac_value is not None
        
        # Verify HMAC
        is_valid = CryptoEngine.verify_hmac(message, hmac_value, key)
        assert is_valid is True
    
    def test_hmac_tampering(self):
        """Test that tampered message fails HMAC verification."""
        key = os.urandom(32)
        message = "Original message"
        tampered_message = "Tampered message"
        
        hmac_value = CryptoEngine.generate_hmac(message, key)
        is_valid = CryptoEngine.verify_hmac(tampered_message, hmac_value, key)
        
        assert is_valid is False
    
    def test_password_hashing(self):
        """Test bcrypt password hashing."""
        password = "SecurePassword123"
        
        # Hash password
        hashed = CryptoEngine.hash_password(password)
        assert hashed is not None
        assert len(hashed) > 0
        
        # Verify correct password
        is_valid = CryptoEngine.verify_password(password, hashed)
        assert is_valid is True
        
        # Verify wrong password
        is_valid = CryptoEngine.verify_password("WrongPassword", hashed)
        assert is_valid is False
    
    def test_password_hash_uniqueness(self):
        """Test that same password generates different hashes."""
        password = "TestPassword"
        
        hash1 = CryptoEngine.hash_password(password)
        hash2 = CryptoEngine.hash_password(password)
        
        # Hashes should be different due to random salt
        assert hash1 != hash2
        
        # But both should verify correctly
        assert CryptoEngine.verify_password(password, hash1)
        assert CryptoEngine.verify_password(password, hash2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

---

### examples/basic_usage.py

```python
"""
Basic usage example for SecureChat.
"""

from src.main import SecureChatSystem


def main():
    print("SecureChat - Basic Usage Example")
    print("=" * 50)
    
    # Initialize chat system
    chat = SecureChatSystem()
    
    # Register users
    print("\n1. Registering users...")
    chat.register_user("Alice", "alice_password_123")
    chat.register_user("Bob", "bob_secure_pass")
    
    # Authenticate
    print("\n2. Authenticating users...")
    if chat.authenticate_user("Alice", "alice_password_123"):
        print("✓ Alice authenticated")
    
    if chat.authenticate_user("Bob", "bob_secure_pass"):
        print("✓ Bob authenticated")
    
    # Send messages
    print("\n3. Sending encrypted messages...")
    msg1 = chat.send_message("Alice", "Bob", "Hi Bob! How are you?")
    msg2 = chat.send_message("Bob", "Alice", "Hi Alice! I'm good, thanks!")
    
    # Read messages
    print("\n4. Reading messages...")
    bob_messages = chat.get_messages_for_user("Bob")
    for msg in bob_messages:
        chat.read_message(msg, "Bob")
    
    alice_messages = chat.get_messages_for_user("Alice")
    for msg in alice_messages:
        chat.read_message(msg, "Alice")
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
```

---

### docs/user_guide.md

```markdown
# SecureChat User Guide

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-team/securechat.git
cd securechat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Features

### User Registration

To register a new account:
1. Click "Register" tab
2. Enter your desired username
3. Enter a strong password (minimum 8 characters)
4. Click "Register" button

Your cryptographic keys are automatically generated during registration.

### Logging In

1. Enter your username
2. Enter your password
3. Click "Login" button

### Sending Messages

1. Select a recipient from the user list
2. Type your message in the input field
3. Press Enter or click "Send"

Your message is automatically:
- Encrypted with AES-256
- Signed with your private key
- Protected with HMAC

### Reading Messages

Messages are automatically decrypted when you select a conversation. 
A green shield icon indicates the message signature is verified.

## Security Best Practices

1. **Strong Passwords**: Use passwords with:
   - At least 8 characters
   - Mix of uppercase and lowercase
   - Numbers and special characters

2. **Device Security**: 
   - Keep your device free from malware
   - Lock your screen when away
   - Don't share your login credentials

3. **Key Protection**:
   - Your private keys never leave your device
   - Don't screenshot or share your keys
   - Log out when finished

## Troubleshooting

### Cannot login
- Verify username and password are correct
- Check caps lock is off
- Try re-registering if account is corrupted

### Messages won't decrypt
- Ensure you're logged in as the recipient
- Check network connection
- Verify sender's account is valid

### Performance issues
- Close other applications
- Clear browser cache
- Restart the application

## Support

For issues or questions:
- Check documentation in `docs/`
- Review code examples in `examples/`
- Contact: adil.akhmetov@sdu.edu.kz
```

---

## 🚀 Setup Instructions

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-team/securechat.git
cd securechat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest src/tests/ -v

# Run application
python src/main.py
```

### For Web Interface

```bash
# Navigate to web directory
cd src/web

# Install npm dependencies
npm install

# Start development server
npm start
```

---

## 📝 Commit Message Guidelines

Use conventional commits:

```
feat: Add ECDH key exchange
fix: Correct signature verification bug
docs: Update security analysis
test: Add encryption unit tests
refactor: Improve key management structure
style: Format code with black
chore: Update dependencies
```

---

## 🔐 Security Checklist Before Submission

- [ ] All passwords hashed with bcrypt
- [ ] No hardcoded secrets or keys
- [ ] Proper error handling implemented
- [ ] Input validation on all user inputs
- [ ] All cryptographic operations documented
- [ ] Security analysis completed
- [ ] Threat model documented
- [ ] Test coverage > 80%
- [ ] Code follows best practices
- [ ] Documentation up to date

---

This complete structure provides everything needed for a professional GitHub repository!