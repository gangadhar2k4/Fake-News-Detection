import requests
import os
import re
from django.conf import settings
from .api_verifier import AutoAPINewsVerifier


class TextPreprocessor:
    """Text preprocessing utility for news articles"""
    
    @staticmethod
    def clean_text(text):
        """Clean and preprocess text data"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        text = re.sub(r'\S+@\S+', '', text)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text


class APINewsVerifier:
    
    def __init__(self):
        self.grok_verifier = AutoAPINewsVerifier()
        self.api_key = os.getenv('NEWS_VERIFICATION_API_KEY')
        self.preprocessor = TextPreprocessor()
        
    def verify_news(self, text, title=""):
        """Verify news using Grok AI or fallback API service"""
        try:
            return self.grok_verifier.verify_news(text, title)
        except Exception as e:
            print(f"Grok verification error: {e}")
            
            if self.api_key:
                return self._legacy_api_verification(text, title)
            else:
                return self._demo_verification(text, title)
    
    def _legacy_api_verification(self, text, title=""):
        """Legacy API verification method"""
        try:
            
            cleaned_text = self.preprocessor.clean_text(text)
            cleaned_title = self.preprocessor.clean_text(title) if title else ""
            
            if not cleaned_text.strip():
                return {
                    'prediction': 'Unable to analyze',
                    'confidence': 0.0,
                    'api_response': None,
                    'error': 'Text is empty or contains no meaningful content'
                }
            
            content_to_verify = f"{cleaned_title} {cleaned_text}".strip()
            
            api_result = self._call_verification_api(content_to_verify)
            
            if api_result.get('error'):
                return api_result
            
            return self._process_api_response(api_result)
            
        except Exception as e:
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'api_response': None,
                'error': f'Verification failed: {str(e)}'
            }
    
    def _call_verification_api(self, content):
        """Make API call to verification service"""
        try:
            api_url = "https://api.example-factcheck.com/verify"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'text': content,
                'language': 'en'
            }
            
            response = requests.post(api_url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    'error': 'Invalid API key. Please check your NEWS_VERIFICATION_API_KEY.'
                }
            elif response.status_code == 429:
                return {
                    'error': 'API rate limit exceeded. Please try again later.'
                }
            else:
                return {
                    'error': f'API request failed with status {response.status_code}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'error': 'API request timed out. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'error': 'Cannot connect to verification service. Please check your internet connection.'
            }
        except Exception as e:
            return {
                'error': f'API call failed: {str(e)}'
            }
    
    def _process_api_response(self, api_response):
        """Process the API response and normalize the format"""
        try:
            
            prediction = api_response.get('verdict', 'Unknown')
            confidence = api_response.get('confidence', 0.5)
            
            label_mapping = {
                'true': 'True',
                'false': 'Fake',
                'mixed': 'Partially True',
                'unverified': 'Partially True',
                'mostly_true': 'True',
                'mostly_false': 'Fake',
                'half_true': 'Partially True'
            }
            
            normalized_prediction = label_mapping.get(prediction.lower(), prediction)
            
            return {
                'prediction': normalized_prediction,
                'confidence': float(confidence),
                'api_response': api_response,
                'error': None
            }
            
        except Exception as e:
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'api_response': api_response,
                'error': f'Failed to process API response: {str(e)}'
            }
    
    def _demo_verification(self, text, title=""):
        """Demo verification system for testing without API key"""
        import random
        import hashlib
        
        try:
            cleaned_text = self.preprocessor.clean_text(text)
            cleaned_title = self.preprocessor.clean_text(title) if title else ""
            
            if not cleaned_text.strip():
                return {
                    'prediction': 'Unable to analyze',
                    'confidence': 0.0,
                    'api_response': None,
                    'error': 'Text is empty or contains no meaningful content'
                }
            
            content_hash = hashlib.md5((cleaned_title + cleaned_text).encode()).hexdigest()
            seed = int(content_hash[:8], 16)
            random.seed(seed)
            
            fake_indicators = ['breaking', 'urgent', 'shocking', 'unbelievable', 'secret', 'exposed']
            true_indicators = ['research', 'study', 'official', 'according to', 'data shows', 'evidence']
            
            text_lower = cleaned_text.lower()
            fake_score = sum(1 for word in fake_indicators if word in text_lower)
            true_score = sum(1 for word in true_indicators if word in text_lower)
            
            if fake_score > true_score:
                prediction = 'Fake'
                base_confidence = 0.6 + random.random() * 0.3
            elif true_score > fake_score:
                prediction = 'True'
                base_confidence = 0.6 + random.random() * 0.3
            else:
                predictions = ['True', 'Fake', 'Partially True']
                prediction = random.choice(predictions)
                base_confidence = 0.5 + random.random() * 0.4
            
            length_factor = min(len(cleaned_text) / 500, 1.0)
            final_confidence = min(base_confidence * (0.7 + length_factor * 0.3), 0.95)
            
            return {
                'prediction': prediction,
                'confidence': final_confidence,
                'api_response': {
                    'demo_mode': True,
                    'message': 'Demo verification - configure NEWS_VERIFICATION_API_KEY for real analysis'
                },
                'error': None
            }
            
        except Exception as e:
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'api_response': None,
                'error': f'Demo verification failed: {str(e)}'
            }


class FakeNewsDetector:
    """Compatibility wrapper for the new API-based system"""
    
    def __init__(self):
        self.api_verifier = APINewsVerifier()
    
    def predict(self, text, title=""):
        """Predict using API verification"""
        result = self.api_verifier.verify_news(text, title)
        
        return {
            'prediction': result.get('prediction', 'Error'),
            'confidence': result.get('confidence', 0.0),
            'logistic_prediction': result.get('prediction', 'Error'),
            'tree_prediction': result.get('prediction', 'Error'),
            'logistic_confidence': result.get('confidence', 0.0),
            'tree_confidence': result.get('confidence', 0.0),
            'error': result.get('error')
        }
