"""
TripX LLM Engine - Natural Language Generation for Travel Recommendations

This module integrates free LLMs and APIs to enhance ML recommendations with:
- Personalized travel itineraries
- Natural language explanations
- Weather validation
- Dynamic attraction data

DESIGN PRINCIPLE: ML remains the decision layer, LLMs only generate text
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time


class TripXLLMEngine:
    """
    LLM-powered text generation engine for travel recommendations.
    
    Separates concerns:
    - ML Engine: Makes recommendation decisions
    - LLM Engine: Generates human-readable content
    - APIs: Provide real-world data enrichment
    """
    
    def __init__(self, llm_provider: str = "local"):
        """
        Initialize LLM engine with specified provider.
        
        Args:
            llm_provider: "groq", "huggingface", or "local" (ollama)
        """
        self.llm_provider = llm_provider
        self.groq_api_key = None  # Set if using Groq
        self.hf_api_key = None    # Set if using HuggingFace
        
        # API endpoints (all free)
        self.weather_api_base = "https://api.open-meteo.com/v1/forecast"
        self.places_api_base = "https://api.opentripmap.com/0.1/en/places"
        
    def get_weather_data(self, destination: str, latitude: float = None, 
                        longitude: float = None) -> Dict:
        """
        Get weather data for destination validation.
        Uses Open-Meteo API (completely free, no API key required).
        
        Args:
            destination: Destination name
            latitude: Destination latitude (if known)
            longitude: Destination longitude (if known)
            
        Returns:
            Weather data dictionary
        """
        try:
            # Default coordinates for major cities (simplified for demo)
            city_coords = {
                "paris": (48.8566, 2.3522),
                "tokyo": (35.6762, 139.6503),
                "new york": (40.7128, -74.0060),
                "london": (51.5074, -0.1278),
                "bangkok": (13.7563, 100.5018),
                "bali": (-8.3405, 115.0920),
                "rome": (41.9028, 12.4964),
                "barcelona": (41.3851, 2.1734),
                "sydney": (-33.8688, 151.2093),
                "dubai": (25.2048, 55.2708)
            }
            
            # Use provided coordinates or lookup
            if latitude and longitude:
                lat, lon = latitude, longitude
            else:
                dest_lower = destination.lower()
                lat, lon = city_coords.get(dest_lower, (40.7128, -74.0060))  # Default to NYC
            
            # Get 7-day forecast
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "timezone": "auto",
                "forecast_days": 7
            }
            
            response = requests.get(self.weather_api_base, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process weather data
                daily = data.get("daily", {})
                weather_summary = {
                    "destination": destination,
                    "avg_temp_max": sum(daily.get("temperature_2m_max", [])) / len(daily.get("temperature_2m_max", [1])),
                    "avg_temp_min": sum(daily.get("temperature_2m_min", [])) / len(daily.get("temperature_2m_min", [1])),
                    "total_precipitation": sum(daily.get("precipitation_sum", [])),
                    "weather_suitable": True,  # Simplified logic
                    "weather_note": "Current weather conditions are favorable for travel"
                }
                
                # Simple suitability logic
                if weather_summary["total_precipitation"] > 50:
                    weather_summary["weather_suitable"] = False
                    weather_summary["weather_note"] = "High precipitation expected - consider indoor activities"
                
                return weather_summary
                
        except Exception as e:
            print(f"Weather API error: {e}")
            
        # Fallback weather data
        return {
            "destination": destination,
            "avg_temp_max": 22,
            "avg_temp_min": 15,
            "total_precipitation": 10,
            "weather_suitable": True,
            "weather_note": "Weather data unavailable - check local forecasts"
        }
    
    def get_attractions(self, destination: str, limit: int = 5) -> List[Dict]:
        """
        Get top attractions for a destination.
        Uses OpenTripMap API (free tier available).
        
        Args:
            destination: Destination name
            limit: Number of attractions to return
            
        Returns:
            List of attraction dictionaries
        """
        try:
            # Simplified attraction data (in real implementation, would use API)
            # OpenTripMap requires API key even for free tier, so using static data
            
            attraction_db = {
                "paris": [
                    {"name": "Eiffel Tower", "type": "landmark", "rating": 4.6},
                    {"name": "Louvre Museum", "type": "museum", "rating": 4.7},
                    {"name": "Notre-Dame Cathedral", "type": "religious", "rating": 4.5},
                    {"name": "Arc de Triomphe", "type": "monument", "rating": 4.5},
                    {"name": "Sacré-Cœur", "type": "religious", "rating": 4.4}
                ],
                "tokyo": [
                    {"name": "Senso-ji Temple", "type": "religious", "rating": 4.3},
                    {"name": "Tokyo Skytree", "type": "landmark", "rating": 4.2},
                    {"name": "Meiji Shrine", "type": "religious", "rating": 4.4},
                    {"name": "Tsukiji Fish Market", "type": "market", "rating": 4.1},
                    {"name": "Imperial Palace", "type": "historical", "rating": 4.2}
                ],
                "new york": [
                    {"name": "Statue of Liberty", "type": "landmark", "rating": 4.5},
                    {"name": "Central Park", "type": "park", "rating": 4.6},
                    {"name": "Times Square", "type": "entertainment", "rating": 4.2},
                    {"name": "Brooklyn Bridge", "type": "landmark", "rating": 4.5},
                    {"name": "9/11 Memorial", "type": "memorial", "rating": 4.7}
                ],
                "london": [
                    {"name": "Big Ben", "type": "landmark", "rating": 4.5},
                    {"name": "Tower of London", "type": "historical", "rating": 4.4},
                    {"name": "British Museum", "type": "museum", "rating": 4.6},
                    {"name": "London Eye", "type": "attraction", "rating": 4.3},
                    {"name": "Buckingham Palace", "type": "palace", "rating": 4.2}
                ]
            }
            
            dest_lower = destination.lower()
            attractions = attraction_db.get(dest_lower, [
                {"name": f"{destination} City Center", "type": "area", "rating": 4.0},
                {"name": f"{destination} Main Square", "type": "landmark", "rating": 4.1},
                {"name": f"Local Museum", "type": "museum", "rating": 3.9},
                {"name": f"Historic District", "type": "historical", "rating": 4.0},
                {"name": f"Cultural Center", "type": "cultural", "rating": 3.8}
            ])
            
            return attractions[:limit]
            
        except Exception as e:
            print(f"Attractions API error: {e}")
            return [{"name": f"{destination} highlights", "type": "general", "rating": 4.0}]
    
    def generate_llm_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using specified LLM provider.
        
        Args:
            prompt: Input prompt for LLM
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            if self.llm_provider == "groq":
                return self._generate_groq(prompt, max_tokens)
            elif self.llm_provider == "huggingface":
                return self._generate_huggingface(prompt, max_tokens)
            else:
                return self._generate_local(prompt, max_tokens)
                
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._generate_fallback(prompt)
    
    def _generate_groq(self, prompt: str, max_tokens: int) -> str:
        """Generate text using Groq API (requires API key)."""
        if not self.groq_api_key:
            return self._generate_fallback(prompt)
            
        # Groq API implementation would go here
        # For now, return fallback
        return self._generate_fallback(prompt)
    
    def _generate_huggingface(self, prompt: str, max_tokens: int) -> str:
        """Generate text using HuggingFace Inference API (free tier)."""
        try:
            # Simple HuggingFace API call (free tier)
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": f"Bearer {self.hf_api_key}"} if self.hf_api_key else {}
            
            payload = {"inputs": prompt, "parameters": {"max_length": max_tokens}}
            
            if self.hf_api_key:
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "").replace(prompt, "").strip()
            
        except Exception as e:
            print(f"HuggingFace API error: {e}")
            
        return self._generate_fallback(prompt)
    
    def _generate_local(self, prompt: str, max_tokens: int) -> str:
        """Generate text using local Ollama (if available)."""
        try:
            # Try to connect to local Ollama instance
            ollama_url = "http://localhost:11434/api/generate"
            payload = {
                "model": "llama2",  # or another available model
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": max_tokens}
            }
            
            response = requests.post(ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
                
        except Exception as e:
            print(f"Local LLM error: {e}")
            
        return self._generate_fallback(prompt)
    
    def _generate_fallback(self, prompt: str) -> str:
        """
        Fallback text generation using template-based approach.
        Used when LLM APIs are unavailable.
        """
        if "itinerary" in prompt.lower():
            return """Day 1: Arrival and City Orientation
- Morning: Arrive and check into accommodation
- Afternoon: Explore the city center and main landmarks
- Evening: Welcome dinner at a local restaurant

Day 2: Cultural Exploration
- Morning: Visit top museums and cultural sites
- Afternoon: Walking tour of historic districts
- Evening: Experience local nightlife and entertainment

Day 3: Local Experiences
- Morning: Local market visit and shopping
- Afternoon: Participate in cultural activities
- Evening: Sunset viewing and photography

This itinerary balances must-see attractions with authentic local experiences."""

        elif "explanation" in prompt.lower():
            return """This destination was recommended based on your preferences for cultural experiences and budget considerations. The location offers excellent value for money with high-quality attractions and safe travel conditions. The timing aligns well with favorable weather patterns and local seasonal highlights."""
        
        else:
            return "Travel recommendation generated based on your preferences and our ML analysis."
    
    def generate_itinerary(self, destination_data: Dict, user_preferences: Dict, 
                          duration: int) -> Dict:
        """
        Generate comprehensive travel itinerary using ML data + LLM + APIs.
        
        Args:
            destination_data: ML-recommended destination info
            user_preferences: User travel preferences
            duration: Trip duration in days
            
        Returns:
            Complete itinerary dictionary
        """
        destination_name = destination_data.get("destination", "Unknown")
        
        # Get enrichment data from APIs
        weather_data = self.get_weather_data(destination_name)
        attractions = self.get_attractions(destination_name)
        
        # Create LLM prompt for itinerary generation
        prompt = f"""Create a {duration}-day travel itinerary for {destination_name}.
        
User preferences:
- Budget: ${user_preferences.get('budget', 100)}/day
- Trip type: {user_preferences.get('trip_type', 'culture')}
- Season: {user_preferences.get('season', 'spring')}

Destination info:
- Cost per day: ${destination_data.get('cost_per_day', 100)}
- Trip type: {destination_data.get('trip_type', 'culture')}
- Best season: {destination_data.get('best_season', 'spring')}

Top attractions: {', '.join([a['name'] for a in attractions[:3]])}

Weather: {weather_data.get('weather_note', 'Check local conditions')}

Generate a day-by-day itinerary with morning, afternoon, and evening activities."""

        # Generate itinerary text using LLM
        itinerary_text = self.generate_llm_text(prompt, max_tokens=800)
        
        # Structure the response
        itinerary = {
            "destination": destination_name,
            "duration": duration,
            "user_preferences": user_preferences,
            "ml_recommendation_score": destination_data.get("overall_score", 0),
            "weather_info": weather_data,
            "top_attractions": attractions,
            "daily_itinerary": itinerary_text,
            "estimated_daily_cost": destination_data.get("cost_per_day", 100),
            "total_estimated_cost": destination_data.get("cost_per_day", 100) * duration,
            "recommendation_explanation": self._generate_explanation(destination_data, user_preferences),
            "travel_tips": self._generate_travel_tips(destination_data, weather_data),
            "generated_at": datetime.now().isoformat()
        }
        
        return itinerary
    
    def _generate_explanation(self, destination_data: Dict, user_preferences: Dict) -> str:
        """Generate explanation for why this destination was recommended."""
        
        prompt = f"""Explain why {destination_data.get('destination')} is recommended for this traveler:

User wants: {user_preferences.get('trip_type')} travel, ${user_preferences.get('budget')}/day budget, {user_preferences.get('duration')} days

Destination offers: {destination_data.get('trip_type')} experience, ${destination_data.get('cost_per_day')}/day cost, {destination_data.get('best_season')} season

ML score: {destination_data.get('overall_score', 0):.3f}

Write a clear, personalized explanation."""

        explanation = self.generate_llm_text(prompt, max_tokens=300)
        
        if not explanation or len(explanation) < 50:
            # Fallback explanation
            explanation = f"""This destination is highly recommended for you because it perfectly matches your {user_preferences.get('trip_type', 'travel')} preferences and ${user_preferences.get('budget', 100)}/day budget. With a recommendation score of {destination_data.get('overall_score', 0):.3f}, it offers excellent value and aligns well with your travel style and timing preferences."""
        
        return explanation
    
    def _generate_travel_tips(self, destination_data: Dict, weather_data: Dict) -> List[str]:
        """Generate practical travel tips based on destination and weather."""
        
        tips = []
        
        # Weather-based tips
        if weather_data.get("total_precipitation", 0) > 30:
            tips.append("Pack waterproof clothing and an umbrella for rainy weather")
        
        if weather_data.get("avg_temp_max", 20) > 30:
            tips.append("Bring sun protection and stay hydrated in hot weather")
        
        if weather_data.get("avg_temp_min", 15) < 10:
            tips.append("Pack warm layers for cool temperatures")
        
        # Destination-based tips
        trip_type = destination_data.get("trip_type", "")
        if trip_type == "culture":
            tips.append("Research local customs and dress codes for cultural sites")
        elif trip_type == "beach":
            tips.append("Don't forget sunscreen and beach essentials")
        elif trip_type == "urban":
            tips.append("Use public transportation and book restaurants in advance")
        elif trip_type == "nature":
            tips.append("Bring appropriate hiking gear and respect wildlife")
        
        # Budget tips
        cost = destination_data.get("cost_per_day", 100)
        if cost < 50:
            tips.append("Great value destination - try local street food and markets")
        elif cost > 150:
            tips.append("Premium destination - consider booking experiences in advance")
        
        return tips[:5]  # Return top 5 tips


def test_llm_engine():
    """Test the LLM engine with sample data."""
    
    print("🤖 Testing TripX LLM Engine")
    print("=" * 50)
    
    # Initialize engine
    engine = TripXLLMEngine(llm_provider="local")  # Try local first, fallback to templates
    
    # Sample ML recommendation data
    sample_destination = {
        "destination": "Paris",
        "country": "France",
        "cost_per_day": 120,
        "trip_type": "culture",
        "best_season": "spring",
        "overall_score": 0.892,
        "explanation": "Perfect match for culture travel with excellent museums and architecture"
    }
    
    # Sample user preferences
    sample_user = {
        "budget": 100,
        "duration": 5,
        "trip_type": "culture",
        "season": "spring"
    }
    
    print(f"Testing with destination: {sample_destination['destination']}")
    print(f"User preferences: {sample_user}")
    
    # Test weather API
    print(f"\n🌤️ Testing Weather API...")
    weather = engine.get_weather_data("Paris")
    print(f"Weather suitable: {weather['weather_suitable']}")
    print(f"Weather note: {weather['weather_note']}")
    
    # Test attractions API
    print(f"\n🏛️ Testing Attractions API...")
    attractions = engine.get_attractions("Paris")
    print(f"Found {len(attractions)} attractions:")
    for attr in attractions[:3]:
        print(f"  - {attr['name']} ({attr['type']}) - Rating: {attr['rating']}")
    
    # Test itinerary generation
    print(f"\n📋 Generating Complete Itinerary...")
    itinerary = engine.generate_itinerary(sample_destination, sample_user, 5)
    
    print(f"\n=== GENERATED ITINERARY ===")
    print(f"Destination: {itinerary['destination']}")
    print(f"Duration: {itinerary['duration']} days")
    print(f"ML Score: {itinerary['ml_recommendation_score']:.3f}")
    print(f"Estimated Cost: ${itinerary['total_estimated_cost']}")
    
    print(f"\n📝 Daily Itinerary:")
    print(itinerary['daily_itinerary'])
    
    print(f"\n💡 Recommendation Explanation:")
    print(itinerary['recommendation_explanation'])
    
    print(f"\n🎯 Travel Tips:")
    for tip in itinerary['travel_tips']:
        print(f"  • {tip}")
    
    print(f"\n✅ LLM Engine Test Complete!")
    
    return itinerary


if __name__ == "__main__":
    # Run test
    test_itinerary = test_llm_engine()
    
    # Save test output
    with open("llm_test_output.json", "w") as f:
        json.dump(test_itinerary, f, indent=2)
    
    print(f"\n📄 Test output saved to 'llm_test_output.json'")