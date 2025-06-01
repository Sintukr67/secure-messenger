# Secure Messenger

A secure messaging system with end-to-end encryption, file sharing capabilities, and message analysis features.

## Features

 **Secure Authentication**
  - User registration and login system
  - Password-based authentication
  - Session management

  **End-to-End Encryption**
  - Message encryption using shared keys
  - Secure file transfer
  - Encrypted message history

   **File Sharing**
  - Secure file transfer between users
  - Encrypted file storage
  - Metadata management for shared files

  **Message Analysis**
  - Content analysis using ML
  - Suspicious content detection
  - Message statistics and insights

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - cryptography
  - scikit-learn
  - numpy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/secure-messenger.git
cd secure-messenger
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Follow the menu options:
   - Register a new account
   - Login to your account
   - Send secure messages
   - Share files securely
   - View received messages
   - View received files
   - Check message statistics

## Security Features

- Messages are encrypted using a shared key derived from both sender and receiver passwords
- Files are encrypted before transfer and storage
- Message content is analyzed for suspicious patterns
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
3. Commit your changes (`git commit -m 'Add some Feature'`)
4. Push to the branch (`git push origin feature`)
5. Open a Pull Request

## Acknowledgments

- Built with Python
- Uses cryptography for secure messaging
- Implements machine learning for message analysis
