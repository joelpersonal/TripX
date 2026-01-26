from typing import Dict, List, Optional
from recsys import create_recommendation_engine
from llm_engine import TravelItineraryGenerator
import json


class TripXIntegratedEngine:
    """
    Integrated engine that combines ML recommendations with LLM text generation and API enrichment.
    
    STRICT ARCHITECTURE:
    1. ML System: Core intelligence for destination recommendations and scoring
    2. LLM Engine: Natural language generation ONLY (no decision making)
    3. API Integration: Data enrichment ONLY (weather, attractions)
    
    The ML system remains the authoritative source for all travel recommendations.
    """
    
    def __init__(self, llm_provider: str = "groq"):
        print("🧠 Loading ML recommendation engine...")
        self.ml_engine, self.destinations_df = create_recommendation_engine('../data/raw/dest.csv')
        
        print("🤖 Loading LLM and API integrations...")
        self.itinerary_generator = TravelItineraryGenerator(llm_provider)
        
        print("✅ Integrated engine ready!")
        print(f"📊 ML Engine: {len(self.destinations_df)} destinations loaded")
        print(f"🤖 LLM Provider: {llm_provider}")
    
    def get_enhanced_recommendations(self, user_preferences: Dict, top_n: int = 3) -> Dict:
        """
        Get ML recommendations enhanced with LLM-generated itineraries and API data.
        
        PROCESS:
        1. ML engine generates recommendations (authoritative)
        2. LLM generates natural language descriptions
        3. APIs provide enrichment data
        """
        
        print("🧠 Generating ML recommendations...")
        user_profile = self.ml_engine.preprocessor.create_user_profile_features(
            budget=user_preferences['budget'],
            duration=user_preferences['duration'],
            trip_type=user_preferences['trip_type'],
            season=user_preferences['season']
        )
        
        ml_recommendations = self.ml_engine.get_recommendations(user_profile, top_n=top_n)
        
        if not ml_recommendations:
            return {
                'status': 'no_recommendations',
                'message': 'No destinations match your criteria',
                'user_preferences': user_preferences
            }
        
        print("🤖 Enhancing with LLM and API data...")
        enhanced_recommendations = []
        
        for i, ml_rec in enumerate(ml_recommendations):
            print(f"   Processing {ml_rec['destination']}...")
            
            itinerary_data = self.itinerary_generator.generate_itinerary(
                user_preferences, [ml_rec]
            )
            
            enhanced_rec = {
                'ml_recommendation': ml_rec,
                'ml_score': ml_rec['overall_score'],
                'ml_reasoning': ml_rec['explanation'],
                'detailed_itinerary': itinerary_data.get('daily_itinerary', ''),
                'llm_explanation': itinerary_data.get('llm_explanation', ''),
                'weather_info': itinerary_data.get('weather_context', {}),
                'attractions': itinerary_data.get('top_attractions', []),
                'rank': i + 1,
                'enhancement_status': 'success'
            }
            
            enhanced_recommendations.append(enhanced_rec)
        
        return {
            'status': 'success',
            'user_preferences': user_preferences,
            'total_recommendations': len(enhanced_recommendations),
            'recommendations': enhanced_recommendations,
            'ml_engine_info': {
                'total_destinations': len(self.destinations_df),
                'scoring_algorithm': 'multi_factor_weighted',
                'features_used': 27
            }
        }
    
    def generate_comparison_report(self, user_preferences: Dict) -> Dict:
        """Generate a comparison report of top destinations with detailed analysis."""
        
        enhanced_data = self.get_enhanced_recommendations(user_preferences, top_n=3)
        
        if enhanced_data['status'] != 'success':
            return enhanced_data
        
        recommendations = enhanced_data['recommendations']
        
        if len(recommendations) < 2:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 2 destinations for comparison'
            }
        
        # Build comparison prompt based on available recommendations
        destinations_text = ""
        for i, rec in enumerate(recommendations, 1):
            destinations_text += f"{i}. {rec['ml_recommendation']['destination']} (Score: {rec['ml_score']:.3f})\n"
        
        comparison_prompt = f"""Compare these top travel destinations for a traveler:
Budget: ${user_preferences['budget']}/day, Duration: {user_preferences['duration']} days
Trip Type: {user_preferences['trip_type']}, Season: {user_preferences['season']}

Destinations:
{destinations_text}

Provide a brief comparison highlighting the unique strengths of each destination."""

        comparison_text = self.itinerary_generator.llm_engine.generate_text(
            comparison_prompt, max_tokens=400
        )
        
        return {
            'status': 'success',
            'user_preferences': user_preferences,
            'top_destinations': [rec['ml_recommendation']['destination'] for rec in recommendations],
            'ml_scores': [rec['ml_score'] for rec in recommendations],
            'comparison_analysis': comparison_text,
            'detailed_recommendations': recommendations
        }


def test_integrated_system():
    """Test the integrated system with sample user profiles"""
    print("🧪 Testing Integrated TripX System")
    print("=" * 60)
    
    engine = TripXIntegratedEngine("groq")
    
    test_profiles = [
        {
            "name": "Budget Cultural Explorer",
            "preferences": {
                "budget": 50,
                "duration": 8,
                "trip_type": "culture",
                "season": "spring"
            }
        },
        {
            "name": "Luxury Beach Vacation",
            "preferences": {
                "budget": 200,
                "duration": 6,
                "trip_type": "beach",
                "season": "winter"
            }
        }
    ]
    
    for profile in test_profiles:
        print(f"\n{'='*60}")
        print(f"🎯 Testing: {profile['name']}")
        print(f"Preferences: {profile['preferences']}")
        print(f"{'='*60}")
        
        results = engine.get_enhanced_recommendations(profile['preferences'], top_n=2)
        
        if results['status'] == 'success':
            print(f"✅ Success! Found {results['total_recommendations']} recommendations")
            
            for i, rec in enumerate(results['recommendations'], 1):
                ml_rec = rec['ml_recommendation']
                print(f"\n--- Recommendation {i} ---")
                print(f"🏛️ Destination: {ml_rec['destination']}, {ml_rec['country']}")
                print(f"🎯 ML Score: {rec['ml_score']:.3f}")
                print(f"💰 Cost: ${ml_rec['cost_per_day']}/day")
                print(f"🧠 ML Reasoning: {rec['ml_reasoning'][:100]}...")
                print(f"🤖 LLM Explanation: {rec['llm_explanation'][:100]}...")
                print(f"🌤️ Weather: {rec['weather_info'].get('current_temp', 'N/A')}°C")
                print(f"🏛️ Attractions: {len(rec['attractions'])} found")
        else:
            print(f"❌ No recommendations: {results.get('message', 'Unknown error')}")
    
    print(f"\n✅ Integrated system test complete!")
    print(f"🏗️ Architecture: ML (decisions) + LLM (text) + APIs (enrichment)")


if __name__ == "__main__":
    test_integrated_system()