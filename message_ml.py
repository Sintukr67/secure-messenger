import re
import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from collections import Counter
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class MessageAnalyzer:
    def __init__(self):
        self.pipeline = None
        self.message_stats = {
            'total_messages': 0,
            'avg_length': 0,
            'common_words': Counter()
        }
        
        # Initialize or load the model
        self.model_path = 'message_classifier.joblib'
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.initialize_model()
    
    def preprocess_text(self, text):
        """Preprocess text for ML analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(nltk.corpus.stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        
        return ' '.join(tokens)
    
    def initialize_model(self):
        """Initialize the ML pipeline"""
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                preprocessor=self.preprocess_text
            )),
            ('classifier', MultinomialNB())
        ])
    
    def train_model(self, messages, labels):
        """Train the ML model with new data"""
        if not self.pipeline:
            self.initialize_model()
        
        # Preprocess messages
        processed_messages = [self.preprocess_text(msg) for msg in messages]
        
        # Train the model
        self.pipeline.fit(processed_messages, labels)
        
        # Save the model
        self.save_model()
    
    def save_model(self):
        """Save the trained model"""
        if self.pipeline:
            joblib.dump(self.pipeline, self.model_path)
    
    def load_model(self):
        """Load a trained model"""
        try:
            self.pipeline = joblib.load(self.model_path)
        except:
            self.initialize_model()
    
    def analyze_message(self, message):
        """Analyze a message using ML"""
        if not self.pipeline:
            self.initialize_model()
        
        # Preprocess the message
        processed_message = self.preprocess_text(message)
        
        # Get prediction probabilities
        try:
            probas = self.pipeline.predict_proba([processed_message])[0]
            predicted_class = self.pipeline.classes_[np.argmax(probas)]
            confidence = np.max(probas)
        except:
            # Fallback if model hasn't been trained
            predicted_class = 'normal'
            confidence = 0.0
        
        # Calculate suspicious score based on content
        suspicious_score = self._calculate_suspicious_score(message)
        
        # Update message statistics
        self._update_stats(message)
        
        return {
            'type': predicted_class,
            'confidence': float(confidence),
            'suspicious_score': suspicious_score
        }
    
    def _calculate_suspicious_score(self, message):
        """Calculate suspicious score based on content analysis"""
        message_lower = message.lower()
        suspicious_patterns = {
            'spam': ['buy now', 'click here', 'free offer', 'winner', 'lottery'],
            'sensitive': ['password', 'credit card', 'ssn', 'bank account'],
            'threat': ['hack', 'attack', 'virus', 'malware', 'exploit']
        }
        
        score = 0
        for category, patterns in suspicious_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    score += 1
        
        return score
    
    def _update_stats(self, message):
        """Update message statistics"""
        self.message_stats['total_messages'] += 1
        words = re.findall(r'\w+', message.lower())
        self.message_stats['common_words'].update(words)
        
        # Update average length
        total_length = self.message_stats['avg_length'] * (self.message_stats['total_messages'] - 1)
        self.message_stats['avg_length'] = (total_length + len(message)) / self.message_stats['total_messages']
    
    def get_message_stats(self):
        """Get current message statistics"""
        return {
            'total_messages': self.message_stats['total_messages'],
            'average_length': self.message_stats['avg_length'],
            'top_words': dict(self.message_stats['common_words'].most_common(10))
        }
    
    def is_suspicious(self, message):
        """Check if a message is suspicious"""
        analysis = self.analyze_message(message)
        return analysis['suspicious_score'] > 2 or analysis['confidence'] > 0.8 