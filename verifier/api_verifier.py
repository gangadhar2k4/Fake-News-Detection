"""
Grok AI News Verification System
Uses xAI's Grok models for intelligent news fact-checking
"""
import json
import requests
from typing import Dict, Any, Optional
from fake_news_detector.settings import NEWS_VERIFICATION_API_KEY

class AutoAPINewsVerifier:
    
    def __init__(self):
        self.api_key = NEWS_VERIFICATION_API_KEY
        # self.base_url = "https://api.x.ai/v1"
        self.base_url = "https://api.groq.com/openai/v1"
        # self.model = "grok-beta"  # Using the main Grok model
        self.model = "llama3-70b-8192"

    def verify_news(self, text: str, title: str = "") -> Dict[str, Any]:

        if not self.api_key:
            return self._demo_verification(text, title)
            
        try:
            return self._call_grok_api(text, title)
        except Exception as e:
            print(f"Grok API error: {e}")
            return self._demo_verification(text, title)
    
    def _call_grok_api(self, text: str, title: str = "") -> Dict[str, Any]:
        
        content = f"Headline: {title}\n\nContent: {text}" if title else text
        
        prompt = f"""
        Analyze this news article for factual accuracy and reliability. Consider:
        1. Factual claims and their verifiability
        2. Source credibility indicators
        3. Bias or misleading language
        4. Logical consistency
        5. Evidence quality

        Article to analyze:
        {content}

        Respond with JSON in this exact format:
        {{
            "prediction": "True" | "Fake" | "Partially True",
            "confidence": 0.85,
            "analysis": "Brief explanation of your assessment",
            "key_issues": ["list", "of", "main", "concerns", "if", "any"],
            "credibility_score": 0.8
        }}
        """
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert fact-checker and news analyst. Analyze news articles for accuracy, bias, and credibility. Always respond with valid JSON."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.3, 
            "max_tokens": 500
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        import re
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)

        # Parse the JSON response
        # try:
        #     analysis = json.loads(content)
        #     return {
        #         'prediction': analysis.get('prediction'),
        #         'confidence': float(analysis.get('confidence', 0.5)),
        #         'analysis': analysis.get('analysis', 'Analysis completed'),
        #         'key_issues': analysis.get('key_issues', []),
        #         'credibility_score': float(analysis.get('credibility_score', 0.5))
        #     }
        # except json.JSONDecodeError:
        #     # Fallback if JSON parsing fails
        #     return {
        #         'prediction': 'Partially True',
        #         'confidence': 0.5,
        #         'analysis': content[:200] + "...",
        #         'key_issues': [],
        #         'credibility_score': 0.5
        #     }

        if json_match:
            analysis = json.loads(json_match.group())
            return {
                'prediction': analysis.get('prediction'),
                'confidence': float(analysis.get('confidence', 0.5)),
                'analysis': analysis.get('analysis', 'Analysis completed'),
                'key_issues': analysis.get('key_issues', []),
                'credibility_score': float(analysis.get('credibility_score', 0.5))
            }
        else:
            return {
                'prediction': 'Partially True',
                'confidence': 0.5,
                'analysis': content[:200] + "...",
                'key_issues': [],
                'credibility_score': 0.5
            }
    
    def _demo_verification(self, text: str, title: str = "") -> Dict[str, Any]:
        """Demo verification for testing without API key"""
        # print("Using demo funtion")
        content = (title + " " + text).lower()
        
        fake_indicators = ['breaking', 'shocking', 'unbelievable', 'doctors hate', 'secret', 'conspiracy']
        true_indicators = ['according to', 'study shows', 'research indicates', 'official statement']
        
        fake_score = sum(1 for indicator in fake_indicators if indicator in content)
        true_score = sum(1 for indicator in true_indicators if indicator in content)
        
        if fake_score > true_score:
            prediction = 'Fake'
            confidence = min(0.8, 0.5 + fake_score * 0.1)
            analysis = "Content contains sensationalized language patterns often associated with misinformation."
        elif true_score > fake_score:
            prediction = 'True'
            confidence = min(0.9, 0.6 + true_score * 0.1)
            analysis = "Content shows signs of factual reporting with credible source references."
        else:
            prediction = 'Partially True'
            confidence = 0.6
            analysis = "Content requires further verification. Mixed signals detected."
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'analysis': analysis,
            'key_issues': ['Demo mode - get XAI_API_KEY for full analysis'],
            'credibility_score': confidence,
        }