from auth import UserAuth
from message_encryption import MessageEncryption
from message_ml import MessageAnalyzer
import os
import json
from datetime import datetime

def main():
    # Initialize systems
    auth = UserAuth()
    encryption = MessageEncryption()
    analyzer = MessageAnalyzer()
    current_user = None
    current_password = None
    
    # Create shared files directory if it doesn't exist
    shared_dir = "shared_files"
    if not os.path.exists(shared_dir):
        os.makedirs(shared_dir)
    
    while True:
        print("\n=== Secure Messaging System ===")
        print("1. Register")
        print("2. Login")
        print("3. Send Secure Message")
        print("4. Send Secure File")
        print("5. View Received Messages")
        print("6. View Received Files")
        print("7. View Message Statistics")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            success, message = auth.register_user(username, password)
            print(message)
            
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            success, message = auth.verify_user(username, password)
            print(message)
            if success:
                current_user = username
                current_password = password
                
        elif choice == "3":
            if not current_user:
                print("Please login first!")
                continue
                
            receiver = input("Enter receiver's username: ")
            if not auth.validate_session(receiver):
                print("Receiver not found!")
                continue
                
            # Get receiver's password for shared key
            receiver_password = input("Enter receiver's password for message sharing: ")
            if not auth.verify_user(receiver, receiver_password)[0]:
                print("Invalid receiver password!")
                continue
                
            message = input("Enter your message: ")
            
            # Analyze message using ML
            analysis = analyzer.analyze_message(message)
            if analyzer.is_suspicious(message):
                print("\nWarning: Message contains suspicious content!")
                print(f"Suspicious score: {analysis['suspicious_score']}")
                proceed = input("Do you want to send this message anyway? (y/n): ")
                if proceed.lower() != 'y':
                    continue
            
            # Generate shared key using both passwords
            shared_key = current_password + receiver_password
            encryption.generate_key(shared_key)
            
            # Create message object with metadata
            message_data = {
                "sender": current_user,
                "receiver": receiver,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis
            }
            
            # Convert message object to string and encrypt
            message_str = json.dumps(message_data)
            encrypted_message = encryption.encrypt_message(message_str)
            
            # Save message to history
            save_message_history(current_user, receiver, encrypted_message)
            
            print("\nMessage sent successfully!")
            print("Message Analysis:")
            print(f"Type: {analysis['type']}")
            print(f"Confidence: {analysis['confidence']:.2f}")
            print(f"Suspicious Score: {analysis['suspicious_score']}")
            
        elif choice == "4":
            if not current_user:
                print("Please login first!")
                continue
                
            receiver = input("Enter receiver's username: ")
            if not auth.validate_session(receiver):
                print("Receiver not found!")
                continue
                
            # Get receiver's password for shared key
            receiver_password = input("Enter receiver's password for file sharing: ")
            if not auth.verify_user(receiver, receiver_password)[0]:
                print("Invalid receiver password!")
                continue
                
            file_path = input("Enter full file path to send: ")
            
            # Verify file exists
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found!")
                continue
            
            # Create a unique filename in shared directory
            original_filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shared_filename = f"{current_user}_{receiver}_{timestamp}_{original_filename}"
            shared_path = os.path.join(shared_dir, shared_filename)
                
            # Generate shared key using both passwords
            shared_key = current_password + receiver_password
            encryption.generate_key(shared_key)
            
            # Create file metadata
            file_data = {
                "sender": current_user,
                "receiver": receiver,
                "filename": original_filename,
                "shared_path": shared_path,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save metadata
            metadata_path = os.path.join(shared_dir, shared_filename + '.metadata')
            with open(metadata_path, 'w') as f:
                json.dump(file_data, f)
            
            try:
                # Copy and encrypt the file to shared directory
                with open(file_path, 'rb') as src, open(shared_path + '.encrypted', 'wb') as dst:
                    file_data = src.read()
                    encrypted_data = encryption.encrypt_message(file_data)
                    dst.write(encrypted_data)
                print(f"\nFile sent successfully!")
            except Exception as e:
                print(f"Error sending file: {str(e)}")
                continue
            
        elif choice == "5":
            if not current_user:
                print("Please login first!")
                continue
                
            print("\nReceived Messages:")
            view_received_messages(current_user, current_password)
            
        elif choice == "6":
            if not current_user:
                print("Please login first!")
                continue
                
            print("\nReceived Files:")
            view_received_files(current_user, current_password)
            
        elif choice == "7":
            if not current_user:
                print("Please login first!")
                continue
                
            print("\nMessage Statistics:")
            stats = analyzer.get_message_stats()
            print(f"Total Messages: {stats['total_messages']}")
            print(f"Average Message Length: {stats['average_length']:.2f} characters")
            print("\nTop 10 Most Common Words:")
            for word, count in stats['top_words'].items():
                print(f"{word}: {count}")
            
        elif choice == "8":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")

def save_message_history(sender, receiver, encrypted_message):
    """Save message to history file"""
    history_file = "message_history.json"
    history = {}
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    
    if sender not in history:
        history[sender] = []
    if receiver not in history:
        history[receiver] = []
        
    history[sender].append({
        "type": "sent",
        "to": receiver,
        "message": encrypted_message.decode(),
        "timestamp": datetime.now().isoformat()
    })
    
    history[receiver].append({
        "type": "received",
        "from": sender,
        "message": encrypted_message.decode(),
        "timestamp": datetime.now().isoformat()
    })
    
    with open(history_file, 'w') as f:
        json.dump(history, f)

def view_received_messages(username, password):
    """View and decrypt received messages"""
    history_file = "message_history.json"
    if not os.path.exists(history_file):
        print("No messages found.")
        return
        
    with open(history_file, 'r') as f:
        history = json.load(f)
        
    if username not in history:
        print("No messages found.")
        return
    
    received_messages = [msg for msg in history[username] if msg['type'] == 'received']
    
    if not received_messages:
        print("No received messages found.")
        return
    
    # Group messages by sender
    messages_by_sender = {}
    for msg in received_messages:
        sender = msg['from']
        if sender not in messages_by_sender:
            messages_by_sender[sender] = []
        messages_by_sender[sender].append(msg)
    
    print(f"\nReceived messages:")
    
    for sender, messages in messages_by_sender.items():
        print(f"\nFrom: {sender}")
        try:
            # Get sender's password once for all messages from this sender
            sender_password = input(f"Enter {sender}'s password to decrypt messages: ")
            
            # Initialize encryption with shared key
            encryption = MessageEncryption()
            shared_key = sender_password + password
            encryption.generate_key(shared_key)
            
            # Decrypt all messages from this sender
            for i, msg in enumerate(messages, 1):
                print(f"\n{i}. Time: {msg['timestamp']}")
                try:
                    # Decrypt the message
                    decrypted_message = encryption.decrypt_message(msg['message'].encode())
                    
                    # Handle both string and binary data
                    if isinstance(decrypted_message, str):
                        try:
                            message_data = json.loads(decrypted_message)
                            print(f"   Message: {message_data['message']}")
                            if 'analysis' in message_data:
                                analysis = message_data['analysis']
                                print(f"   Type: {analysis['type']}")
                                print(f"   Confidence: {analysis['confidence']:.2f}")
                                print(f"   Suspicious Score: {analysis['suspicious_score']}")
                        except json.JSONDecodeError:
                            print(f"   Message: {decrypted_message}")
                    else:
                        print(f"   Message: [Binary data]")
                except Exception as e:
                    print(f"   Status: Could not decrypt message {i}")
                    print(f"   Error: {str(e)}")
                    
        except Exception as e:
            print(f"   Status: Could not decrypt messages from {sender}")
            print(f"   Error: {str(e)}")

def view_received_files(username, password):
    """View and decrypt received files"""
    shared_dir = "shared_files"
    if not os.path.exists(shared_dir):
        print("No received files found.")
        return
        
    # Look for .metadata files in shared directory
    metadata_files = [f for f in os.listdir(shared_dir) if f.endswith('.metadata')]
    
    if not metadata_files:
        print("No received files found.")
        return
    
    # Filter metadata files for this user
    user_files = []
    for metadata_file in metadata_files:
        try:
            with open(os.path.join(shared_dir, metadata_file), 'r') as f:
                metadata = json.load(f)
                if metadata.get('receiver') == username:
                    user_files.append((metadata_file, metadata))
        except Exception as e:
            continue
    
    if not user_files:
        print("No received files found.")
        return
    
    print(f"\nReceived files:")
    
    for i, (metadata_file, metadata) in enumerate(user_files, 1):
        print(f"\n{i}. From: {metadata['sender']}")
        print(f"   File: {metadata['filename']}")
        
        # Get the corresponding encrypted file
        encrypted_file = os.path.join(shared_dir, metadata_file.replace('.metadata', '.encrypted'))
        if not os.path.exists(encrypted_file):
            continue
        
        try:
            # Get sender's password for shared key
            sender_password = input(f"Enter {metadata['sender']}'s password to decrypt: ")
            
            # Initialize encryption with shared key
            encryption = MessageEncryption()
            shared_key = sender_password + password
            encryption.generate_key(shared_key)
            
            # Decrypt the file
            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = encryption.decrypt_message(encrypted_data)
            
            # Save decrypted file
            decrypted_path = os.path.join(shared_dir, f"decrypted_{metadata['filename']}")
            with open(decrypted_path, 'wb') as f:
                if isinstance(decrypted_data, str):
                    f.write(decrypted_data.encode())
                else:
                    f.write(decrypted_data)
            print(f"   Status: Decrypted successfully")
            print(f"   Saved as: {decrypted_path}")
        except Exception as e:
            print(f"   Status: Could not decrypt")
            print(f"   Error: {str(e)}")

if __name__ == "__main__":
    main() 