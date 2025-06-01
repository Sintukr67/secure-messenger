# Secure Messenger

A secure messaging system with end-to-end encryption, file sharing capabilities, and message analysis features.

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/secure-messenger.git
cd secure-messenger

# Install required packages
pip install -r requirements.txt
```

### 2. Running the Application

```bash
python main.py
```

### 3. Step-by-Step Usage Example

Let's say you want to send a secure message between two users:

1. **Register First User**
   - Select option `1` (Register)
   - Enter username (e.g., `Sintukr`)
   - Enter password (e.g., `@123`)

2. **Register Second User**
   - Select option `1` (Register)
   - Enter username (e.g., `Piyushkr`)
   - Enter password (e.g., `$123`)

3. **Send a Message**
   - Login as Sintukr (option `2`)
   - Select option `3` (Send Secure Message)
   - Enter Piyushkr's username
   - Enter your message
   - The system will analyse and encrypt your message

4. **Read the Message**
   - Login as Piyushkr (option `2`)
   - Select option `5` (View Received Messages)
   - Enter Sintukr's password when prompted
   - View the decrypted message

## Features

 **Secure Authentication**
  - User registration and login
  - Password protection
  - Session management

  **End-to-End Encryption**
  - Messages encrypted using shared keys
  - Secure file transfer
  - Encrypted message history

  **File Sharing**
  - Send encrypted files
  - Secure file storage
  - File metadata management

   **Message Analysis**
  - ML-based content analysis
  - Suspicious content detection
  - Message statistics

## System Requirements

- Python 3.x
- Required packages (automatically installed via requirements.txt):
  - cryptography
  - scikit-learn
  - numpy
  - nltk
  - pandas
  - joblib

## Important Notes

1. This is a **desktop application**, not a web application
2. It runs locally on your computer
3. To communicate, both users need to:
   - Have the application installed
   - Be registered in the system
   - Know each other's passwords for message sharing

## Security Features

- Messages are encrypted using a shared key derived from both sender and receiver passwords
- Files are encrypted before transfer and storage
- Message content is analysed for suspicious patterns
- Secure session management
- Encrypted message history

## Project Structure

```
secure-messenger/
├── main.py              # Main application file
├── auth.py             # Authentication module
├── message_encryption.py # Encryption module
├── message_ml.py       # Message analysis module
├── shared_files/       # Directory for shared files
└── message_history.json # Encrypted message history
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature')
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
