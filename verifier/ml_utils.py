import os
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import re
import string
from django.conf import settings


class TextPreprocessor:
    """Text preprocessing utility for news articles"""
    
    @staticmethod
    def clean_text(text):
        """Clean and preprocess text data"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove punctuation except periods and exclamation marks
        text = re.sub(r'[^\w\s\.\!]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove very short words (less than 2 characters)
        words = text.split()
        words = [word for word in words if len(word) > 2]
        
        return ' '.join(words)


class FakeNewsDetector:
    """Main class for fake news detection using ML models"""
    
    def __init__(self):
        self.models_dir = settings.ML_MODELS_DIR
        self.vectorizer = None
        self.logistic_model = None
        self.decision_tree_model = None
        self.preprocessor = TextPreprocessor()
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models and vectorizer"""
        try:
            vectorizer_path = os.path.join(self.models_dir, 'tfidf_vectorizer.joblib')
            logistic_path = os.path.join(self.models_dir, 'logistic_regression_model.joblib')
            tree_path = os.path.join(self.models_dir, 'decision_tree_model.joblib')
            
            if all(os.path.exists(path) for path in [vectorizer_path, logistic_path, tree_path]):
                self.vectorizer = joblib.load(vectorizer_path)
                self.logistic_model = joblib.load(logistic_path)
                self.decision_tree_model = joblib.load(tree_path)
                print("Models loaded successfully!")
            else:
                print("Models not found. Training new models...")
                self.train_models()
                
        except Exception as e:
            print(f"Error loading models: {e}")
            self.train_models()
    
    def train_models(self):
        """Train new models with sample data"""
        try:
            from ml_models.sample_data import get_sample_data
            
            # Get sample training data
            data = get_sample_data()
            
            if data.empty:
                raise ValueError("No training data available")
            
            # Preprocess text data
            data['cleaned_text'] = data['text'].apply(self.preprocessor.clean_text)
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                data['cleaned_text'], 
                data['label'], 
                test_size=0.2, 
                random_state=42,
                stratify=data['label']
            )
            
            # Create and train TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )
            
            X_train_vectorized = self.vectorizer.fit_transform(X_train)
            X_test_vectorized = self.vectorizer.transform(X_test)
            
            # Train Logistic Regression
            self.logistic_model = LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced'
            )
            self.logistic_model.fit(X_train_vectorized, y_train)
            
            # Train Decision Tree
            self.decision_tree_model = DecisionTreeClassifier(
                random_state=42,
                max_depth=10,
                min_samples_split=5,
                class_weight='balanced'
            )
            self.decision_tree_model.fit(X_train_vectorized, y_train)
            
            # Evaluate models
            lr_pred = self.logistic_model.predict(X_test_vectorized)
            dt_pred = self.decision_tree_model.predict(X_test_vectorized)
            
            print(f"Logistic Regression Accuracy: {accuracy_score(y_test, lr_pred):.3f}")
            print(f"Decision Tree Accuracy: {accuracy_score(y_test, dt_pred):.3f}")
            
            # Save models
            self.save_models()
            
        except Exception as e:
            print(f"Error training models: {e}")
            # Create dummy models as fallback
            self.create_dummy_models()
    
    def create_dummy_models(self):
        """Create dummy models as fallback"""
        from sklearn.dummy import DummyClassifier
        
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        # Fit with dummy data
        dummy_texts = ["This is real news", "This is fake news"]
        self.vectorizer.fit(dummy_texts)
        
        self.logistic_model = DummyClassifier(strategy='uniform', random_state=42)
        self.decision_tree_model = DummyClassifier(strategy='uniform', random_state=42)
        
        # Fit dummy models
        dummy_X = self.vectorizer.transform(dummy_texts)
        dummy_y = ['Real', 'Fake']
        
        self.logistic_model.fit(dummy_X, dummy_y)
        self.decision_tree_model.fit(dummy_X, dummy_y)
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            os.makedirs(self.models_dir, exist_ok=True)
            
            joblib.dump(self.vectorizer, os.path.join(self.models_dir, 'tfidf_vectorizer.joblib'))
            joblib.dump(self.logistic_model, os.path.join(self.models_dir, 'logistic_regression_model.joblib'))
            joblib.dump(self.decision_tree_model, os.path.join(self.models_dir, 'decision_tree_model.joblib'))
            
            print("Models saved successfully!")
            
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def predict(self, text):
        """Predict if news is fake or real using both models"""
        try:
            # Preprocess the input text
            cleaned_text = self.preprocessor.clean_text(text)
            
            if not cleaned_text.strip():
                return {
                    'prediction': 'Unable to analyze',
                    'confidence': 0.0,
                    'logistic_prediction': 'Unable to analyze',
                    'tree_prediction': 'Unable to analyze',
                    'logistic_confidence': 0.0,
                    'tree_confidence': 0.0,
                    'error': 'Text is empty or contains no meaningful content'
                }
            
            # Vectorize the text
            text_vectorized = self.vectorizer.transform([cleaned_text])
            
            # Get predictions from both models
            lr_prediction = self.logistic_model.predict(text_vectorized)[0]
            dt_prediction = self.decision_tree_model.predict(text_vectorized)[0]
            
            # Get prediction probabilities if available
            lr_confidence = 0.5
            dt_confidence = 0.5
            
            if hasattr(self.logistic_model, 'predict_proba'):
                lr_proba = self.logistic_model.predict_proba(text_vectorized)[0]
                lr_confidence = max(lr_proba)
            
            if hasattr(self.decision_tree_model, 'predict_proba'):
                dt_proba = self.decision_tree_model.predict_proba(text_vectorized)[0]
                dt_confidence = max(dt_proba)
            
            # Combine predictions
            predictions = [lr_prediction, dt_prediction]
            confidences = [lr_confidence, dt_confidence]
            
            # Map predictions to standard labels
            label_mapping = {
                'Real': 'True',
                'Fake': 'Fake',
                'REAL': 'True',
                'FAKE': 'Fake',
                'real': 'True',
                'fake': 'Fake',
                'True': 'True',
                'False': 'Fake'
            }
            
            mapped_predictions = [label_mapping.get(pred, pred) for pred in predictions]
            
            # Determine final prediction
            if mapped_predictions[0] == mapped_predictions[1]:
                final_prediction = mapped_predictions[0]
                final_confidence = (confidences[0] + confidences[1]) / 2
            else:
                # If models disagree, choose based on higher confidence
                if confidences[0] > confidences[1]:
                    final_prediction = mapped_predictions[0]
                    final_confidence = confidences[0]
                else:
                    final_prediction = mapped_predictions[1]
                    final_confidence = confidences[1]
                
                # If confidence is low and models disagree, mark as partially true
                if max(confidences) < 0.7:
                    final_prediction = 'Partially True'
                    final_confidence = max(confidences)
            
            return {
                'prediction': final_prediction,
                'confidence': final_confidence,
                'logistic_prediction': label_mapping.get(lr_prediction, lr_prediction),
                'tree_prediction': label_mapping.get(dt_prediction, dt_prediction),
                'logistic_confidence': lr_confidence,
                'tree_confidence': dt_confidence,
                'error': None
            }
            
        except Exception as e:
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'logistic_prediction': 'Error',
                'tree_prediction': 'Error',
                'logistic_confidence': 0.0,
                'tree_confidence': 0.0,
                'error': str(e)
            }
