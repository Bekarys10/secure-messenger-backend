from .chat_system import SecureChatSystem

def demo():
    """
    Demonstration of SecureChat functionality.
    
    Shows:
    - User registration
    - Authentication
    - Secure messaging
    - Signature verification
    """
    print("=" * 60)
    print("SecureChat - Cryptography Project Demo")
    print("Team: Bekarys, Aslan, Bekbol")
    print("Course: MAT364")
    print("=" * 60)
    
    # Initialize system
    chat = SecureChatSystem()
    
    print("\n1️⃣  REGISTRATION PHASE")
    print("-" * 60)
    chat.register_user("Bekarys", "secure_password_123")
    chat.register_user("Aslan", "another_secure_pass")
    chat.register_user("Bekbol", "cryptography_rocks")
    
    print("\n2️⃣  AUTHENTICATION PHASE")
    print("-" * 60)
    if chat.authenticate_user("Bekarys", "secure_password_123"):
        print("✅ Bekarys authenticated successfully")
    
    if not chat.authenticate_user("Aslan", "wrong_password"):
        print("❌ Authentication failed with wrong password (expected)")
    
    if chat.authenticate_user("Aslan", "another_secure_pass"):
        print("✅ Aslan authenticated successfully")
    
    print("\n3️⃣  SECURE MESSAGING PHASE")
    print("-" * 60)
    
    # Send messages
    msg1 = chat.send_message(
        "Bekarys", 
        "Aslan", 
        "Hey Aslan! Our cryptography project is working great!"
    )
    
    msg2 = chat.send_message(
        "Aslan",
        "Bekbol",
        "Bekbol, check out the security analysis document!"
    )
    
    msg3 = chat.send_message(
        "Bekbol",
        "Bekarys",
        "The encryption implementation looks solid!"
    )
    
    print("\n4️⃣  MESSAGE READING PHASE")
    print("-" * 60)
    
    # Read messages
    aslan_messages = chat.get_messages_for_user("Aslan")
    for msg in aslan_messages:
        chat.read_message(msg, "Aslan")
    
    bekbol_messages = chat.get_messages_for_user("Bekbol")
    for msg in bekbol_messages:
        chat.read_message(msg, "Bekbol")
    
    bekarys_messages = chat.get_messages_for_user("Bekarys")
    for msg in bekarys_messages:
        chat.read_message(msg, "Bekarys")
    
    print("\n5️⃣  SECURITY DEMONSTRATION")
    print("-" * 60)
    print("✅ All messages encrypted with AES-256-GCM")
    print("✅ Perfect forward secrecy via ECDH")
    print("✅ Message authenticity via ECDSA signatures")
    print("✅ Integrity protection via HMAC-SHA256")
    print("✅ Secure password storage via bcrypt")
    print("\n" + "=" * 60)
    print("Demo completed successfully! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    demo()

