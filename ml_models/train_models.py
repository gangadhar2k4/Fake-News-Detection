#!/usr/bin/env python
"""
Training script for fake news detection models.
Run this script to train and save the ML models.
"""

import os
import sys
import django
from pathlib import Path

# Add the parent directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_news_detector.settings')
django.setup()

from verifier.ml_utils import FakeNewsDetector
from sample_data import get_sample_data, get_additional_training_data
import pandas as pd


def main():
    """Main training function"""
    print("Starting fake news detection model training...")
    
    # Initialize detector
    detector = FakeNewsDetector()
    
    # Get training data
    print("Loading training data...")
    sample_data = get_sample_data()
    additional_data = get_additional_training_data()
    
    # Combine datasets
    full_data = pd.concat([sample_data, additional_data], ignore_index=True)
    
    print(f"Total training samples: {len(full_data)}")
    print(f"Real news samples: {len(full_data[full_data['label'] == 'Real'])}")
    print(f"Fake news samples: {len(full_data[full_data['label'] == 'Fake'])}")
    
    # Save the combined dataset for reference
    dataset_path = os.path.join(BASE_DIR, 'ml_models', 'training_data.csv')
    full_data.to_csv(dataset_path, index=False)
    print(f"Training data saved to: {dataset_path}")
    
    # Train models
    print("Training models...")
    try:
        # The FakeNewsDetector will automatically train models if they don't exist
        # or we can force retraining by deleting existing models
        models_dir = detector.models_dir
        
        # Remove existing models to force retraining
        model_files = [
            'tfidf_vectorizer.joblib',
            'logistic_regression_model.joblib',
            'decision_tree_model.joblib'
        ]
        
        for model_file in model_files:
            model_path = os.path.join(models_dir, model_file)
            if os.path.exists(model_path):
                os.remove(model_path)
                print(f"Removed existing model: {model_file}")
        
        # Now initialize detector which will train new models
        detector = FakeNewsDetector()
        
        print("Models trained and saved successfully!")
        
        # Test the models with sample predictions
        print("\nTesting models with sample predictions:")
        
        test_texts = [
            "Scientists at major university discover breakthrough in renewable energy technology.",
            "Local man uses this one weird trick to become millionaire overnight, banks hate him!",
            "Government announces new policy to support small businesses during economic recovery.",
            "Shocking revelation: All celebrities are actually aliens from outer space controlling our minds."
        ]
        
        for i, text in enumerate(test_texts, 1):
            result = detector.predict(text)
            print(f"\nTest {i}: {text[:60]}...")
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"Logistic Regression: {result['logistic_prediction']} ({result['logistic_confidence']:.3f})")
            print(f"Decision Tree: {result['tree_prediction']} ({result['tree_confidence']:.3f})")
            
            if result['error']:
                print(f"Error: {result['error']}")
        
        print("\nTraining completed successfully!")
        
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
