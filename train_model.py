from message_ml import MessageAnalyzer
import json

def load_training_data():
    """Load or create sample training data"""
    # Sample training data
    training_data = {
        'messages': [
            "Urgent: Please respond immediately to this message",
            "Hi there, how are you doing?",
            "Dear Sir/Madam, I am writing to inquire about...",
            "What time is the meeting tomorrow?",
            "This is a normal message without any special characteristics",
            "Buy now! Limited time offer! Click here to win!",
            "Please provide your credit card details for verification",
            "I need your password to fix the system",
            "There's a virus in the system that needs immediate attention",
            "Hello, just checking in to see how things are going",
            "Kindly review the attached documents at your earliest convenience",
            "When can we schedule the next team meeting?",
            "Free money! Click here to claim your prize!",
            "Your account has been compromised, please verify your SSN",
            "The system has been hacked, we need to take action"
        ],
        'labels': [
            'urgent',
            'casual',
            'formal',
            'question',
            'normal',
            'spam',
            'sensitive',
            'sensitive',
            'threat',
            'casual',
            'formal',
            'question',
            'spam',
            'sensitive',
            'threat'
        ]
    }
    return training_data

def main():
    # Initialize the analyzer
    analyzer = MessageAnalyzer()
    
    # Load training data
    training_data = load_training_data()
    
    # Train the model
    print("Training the message classifier...")
    analyzer.train_model(training_data['messages'], training_data['labels'])
    print("Training completed!")
    
    # Test the model
    print("\nTesting the model with some examples:")
    test_messages = [
        "Hello, how are you?",
        "URGENT: System maintenance required",
        "Please provide your bank account details",
        "What's the status of the project?",
        "Free iPhone! Click here to claim!"
    ]
    
    for message in test_messages:
        analysis = analyzer.analyze_message(message)
        print(f"\nMessage: {message}")
        print(f"Type: {analysis['type']}")
        print(f"Confidence: {analysis['confidence']:.2f}")
        print(f"Suspicious Score: {analysis['suspicious_score']}")

if __name__ == "__main__":
    main() 