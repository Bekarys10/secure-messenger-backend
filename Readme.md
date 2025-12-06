# SecureChat - End-to-End Encrypted Messaging Application

## 📋 Project Information
- **Course**: MAT364 - Cryptography
- **Instructor**: Adil Akhmetov
- **University**: SDU
- **Project Option**: Option 1 - Secure Messaging Application

## 👥 Team Members
- **Bekarys** (GitHub: @Bekarys10) - Cryptography Implementation & Backend Logic
- **Aslan** (GitHub: @Asik062) - Frontend Development & UI/UX Design
- **Bekbol** (GitHub: @bekbull) - Security Analysis & Documentation

## 🎯 Project Description

SecureChat is an end-to-end encrypted messaging application that demonstrates practical implementation of multiple cryptographic concepts. The application provides secure user authentication, encrypted message transmission, and integrity verification using industry-standard cryptographic algorithms.

## ✨ Features

### Core Features
- ✅ **End-to-End Encryption**: Messages encrypted with AES-256
- ✅ **Secure Key Exchange**: ECDH (Elliptic Curve Diffie-Hellman) protocol
- ✅ **User Authentication**: Password hashing with bcrypt simulation
- ✅ **Digital Signatures**: ECDSA for message integrity verification
- ✅ **Message Integrity**: HMAC-SHA256 for tamper detection
- ✅ **Key Management**: RSA-2048 for secure key encryption

### Additional Features
- 👤 User registration and login system
- 💬 Real-time messaging interface
- 🔑 Public/private key pair generation
- 🛡️ Signature verification indicators
- 📋 Key copying functionality
- 🎨 Modern, responsive UI

## 🔐 Cryptographic Components

### 1. Symmetric Encryption - AES-256
```javascript
static aesEncrypt(message, key) {
  // Encrypts message content using AES-256
  // Key derived from ECDH shared secret
}
```

### 2. Asymmetric Encryption - RSA-2048
```javascript
static generateRSAKeyPair() {
  // Generates 2048-bit RSA key pairs
  // Used for secure key exchange
}
```

### 3. Key Exchange - ECDH
```javascript
static deriveSharedSecret(privateKey, publicKey) {
  // Derives shared secret using ECDH
  // Enables perfect forward secrecy
}
```

### 4. Digital Signatures - ECDSA
```javascript
static sign(message, privateKey) {
  // Creates digital signature for authentication
  // Verifies message sender identity
}
```

### 5. Hash Functions - SHA-256
```javascript
static hashSHA256(data) {
  // Cryptographic hash for integrity
  // Used in HMAC and signatures
}
```

### 6. Password Hashing - bcrypt
```javascript
static hashPassword(password) {
  // Secure password storage
  // Salt generation and iteration
}
```

### 7. Message Authentication - HMAC
```javascript
static hmac(message, key) {
  // Ensures message integrity
  // Prevents tampering
}
```

## 🚀 Installation

### Prerequisites
- Node.js 16+ or Python 3.8+
- Modern web browser
- Git

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-team/securechat.git
cd securechat

# For React version (recommended)
npm install
npm start

# For Python version
pip install -r requirements.txt
python app.py
```

## 📖 Usage Guide

### 1. Registration
1. Click "Register" tab
2. Enter desired username and password
3. System generates RSA and ECDH key pairs automatically
4. Click "Register" button

### 2. Login
1. Enter username and password
2. System verifies credentials using bcrypt
3. Access granted to messaging interface

**Demo Accounts Available:**
- Username: `Bekarys` / Password: `demo123`
- Username: `Aslan` / Password: `demo123`
- Username: `Bekbol` / Password: `demo123`

### 3. Sending Messages
1. Select recipient from user list
2. Type message in input field
3. Click "Send" or press Enter
4. Message is automatically:
   - Encrypted with AES-256
   - Signed with ECDSA
   - Protected with HMAC

### 4. Receiving Messages
- Messages automatically decrypted using shared secret
- Signature verification shown with shield icon
- Timestamp and encryption details displayed

## 🏗️ Architecture

### System Flow
```
User A                          Server                       User B
  |                               |                            |
  |-- Register/Login ------------>|                            |
  |<- Generate Keys --------------|                            |
  |                               |<-- Register/Login ---------|
  |                               |--- Generate Keys --------->|
  |                               |                            |
  |-- ECDH Public Key ----------->|                            |
  |                               |<-- ECDH Public Key --------|
  |-- Derive Shared Secret        |    Derive Shared Secret ---|
  |                               |                            |
  |-- Encrypt with AES-256 ------>|                            |
  |-- Sign with ECDSA ----------->|                            |
  |-- Add HMAC ------------------>|                            |
  |                               |-- Forward Message -------->|
  |                               |<-- Verify HMAC ------------|
  |                               |<-- Verify Signature -------|
  |                               |<-- Decrypt with AES -------|
```

### Component Architecture
```
SecureChat Application
│
├── Authentication Module
│   ├── User Registration
│   ├── Password Hashing (bcrypt)
│   └── Login Verification
│
├── Key Management
│   ├── RSA Key Generation
│   ├── ECDH Key Generation
│   └── Shared Secret Derivation
│
├── Encryption Engine
│   ├── AES-256 Encryption
│   ├── AES-256 Decryption
│   └── Key Derivation (PBKDF2)
│
├── Signature System
│   ├── ECDSA Signing
│   ├── Signature Verification
│   └── HMAC Generation
│
└── User Interface
    ├── Login/Register Forms
    ├── User List
    ├── Chat Interface
    └── Key Display
```

## 🔒 Security Analysis

### Threat Model

#### Threats Considered:
1. **Eavesdropping**: Attacker intercepts messages
   - **Mitigation**: End-to-end encryption with AES-256
   
2. **Man-in-the-Middle (MITM)**: Attacker intercepts key exchange
   - **Mitigation**: ECDH with digital signatures
   
3. **Message Tampering**: Attacker modifies messages
   - **Mitigation**: HMAC-SHA256 and digital signatures
   
4. **Replay Attacks**: Attacker resends old messages
   - **Mitigation**: Timestamps and session management
   
5. **Password Attacks**: Brute force or dictionary attacks
   - **Mitigation**: bcrypt with salt and iterations

### Security Assumptions
- Users protect their private keys
- System random number generator is secure
- Cryptographic libraries are correctly implemented
- No malware on user devices

### Known Limitations
⚠️ **Educational Implementation**: This is a simplified demonstration
- Uses simulated cryptography for learning purposes
- Production use requires established libraries
- No persistent storage (in-memory only)
- Limited to browser environment

### Recommended Improvements for Production
1. Use established libraries: `cryptography.js`, `libsodium`
2. Implement certificate pinning
3. Add multi-factor authentication
4. Implement key rotation
5. Add secure key backup/recovery
6. Use hardware security modules (HSM)
7. Implement perfect forward secrecy
8. Add audit logging

## 📊 Technical Implementation Details

### Key Derivation Flow
```
Password → Salt → PBKDF2 (10,000 iterations) → Derived Key
                                               ↓
                                        AES Encryption Key
```

### Message Encryption Flow
```
1. Sender generates ECDH key pair
2. Receiver generates ECDH key pair
3. Exchange public keys
4. Derive shared secret
5. Encrypt message with AES-256
6. Sign with ECDSA private key
7. Generate HMAC
8. Transmit encrypted message + signature + HMAC
9. Receiver verifies HMAC
10. Receiver verifies signature
11. Receiver decrypts with shared secret
```

### Data Structures
```javascript
User Object:
{
  passwordHash: { hash: string, salt: string },
  keyPair: { privateKey: string, publicKey: string },
  ecdhKeyPair: { privateKey: string, publicKey: string }
}

Message Object:
{
  id: number,
  from: string,
  to: string,
  encryptedContent: string,
  signature: string,
  hmac: string,
  timestamp: string,
  sharedSecret: string
}
```

## 🧪 Testing

### Manual Testing Checklist
- ✅ User registration with valid credentials
- ✅ User registration with duplicate username (should fail)
- ✅ Login with correct credentials
- ✅ Login with incorrect credentials (should fail)
- ✅ Send message between two users
- ✅ Verify message encryption
- ✅ Verify signature validation
- ✅ Verify HMAC integrity
- ✅ Key copying functionality
- ✅ Multiple concurrent conversations

### Test Scenarios
```javascript
// Test 1: Registration
1. Register user "TestUser" with password "test123"
2. Verify keys are generated
3. Verify password is hashed

// Test 2: Message Encryption
1. Login as User A
2. Send message to User B
3. Verify message is encrypted
4. Login as User B
5. Verify message can be decrypted
6. Verify signature is valid

// Test 3: Security
1. Attempt to decrypt message without key
2. Verify decryption fails
3. Attempt to forge signature
4. Verify verification fails
```

## 📚 Documentation Files

- `README.md` - This file
- `architecture.md` - Detailed system architecture
- `security.md` - Complete security analysis
- `API.md` - Function documentation
- `CONTRIBUTING.md` - Contribution guidelines

## 🔧 Technology Stack

- **Frontend**: React 18+ with Hooks
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Cryptography**: Custom implementation (educational)
- **State Management**: React useState

## 🎓 Learning Outcomes

This project demonstrates understanding of:
1. Symmetric and asymmetric encryption
2. Key exchange protocols
3. Digital signatures and message authentication
4. Hash functions and their applications
5. Secure password storage
6. Cryptographic best practices
7. Security threat modeling

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📧 Contact

- **Instructor**: adil.akhmetov@sdu.edu.kz
- **Project Repository**: [https://github.com/bekbull/secure-messenger-backend]
- **Course**: MAT364 - Cryptography

## 🙏 Acknowledgments

- SDU University
- MAT364 Course Materials
- NIST Cryptographic Standards
- OWASP Security Guidelines

---

**Note**: This is an educational project demonstrating cryptographic concepts. For production use, always use established, audited cryptographic libraries and follow industry best practices.
