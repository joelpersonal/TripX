"""
TripX Integrated Engine - Combines ML Recommendations with LLM Enhancement

This module demonstrates the proper separation of concerns:
1. ML Engine: Makes data-driven recommendation decisions
2. LLM Engine: Generates human-readable content and explanations
3. API Layer: Provides real-world data enrichment

ARCHITECTURE PRINCIPLE: ML drives decisions, LLM enhances presentation
"""

from typing import Dict, List, Optional
from recsys import create_recommendation_engine
from llm_engine import TripXLLMEngine
import json


class TripXIntegratedEngine:
    """
    Integrated recommendation system combining ML decision-making with LLM enhancement.
    
    Design Philosophy:
    - ML Engine: Core recommendation logic and scoring
    - LLM Engine: Natural language generation and explanation
    - Clear separation prevents LLM hallucinations from affecting recommendations
    """
    
    def __init__(self, data_path: str = 'data/raw/dest.csv', llm_provider: str = "local"):
        """
        Initialize integrated engine with ML and LLM components.
        
        Args:
            data_path: Path to destination dataset
            llm_provider: LLM provider ("groq", "huggingface", or "local")
        """
        print("🚀 Initializing TripX Integrated Engine...")
        
        # Initialize ML recommendation engine (core decision layer)
        self.ml_engine, self.destinations_df = create_recommendation_engine(data_path)
        print(f"✅ ML Engine loaded with {len(self.destinations_df)} destinations")
        
        # Initialize LLM engine (text generation layer)
        self.llm_engine = TripXLLMEngine(llm_provider=llm_provider)
        print(f"✅ LLM Engine initialized with provider: {llm_provider}")
        
        print("🎯 Integration complete - ML drives decisions, LLM enhances presentation")
    
    def get_enhanced_recommendations(self, user_preferences: Dict, 
                                   num_recommendations: int = 3) -> List[Dict]:
        """
        Get ML-driven recommendations enhanced with LLM-generated content.
        
        Process:
        1. ML Engine generates ranked recommendations
        2. LLM Engine creates itineraries and explanations
        3. APIs provide weather and attraction data
        
        Args:
            user_preferences: User travel preferences
            num_recommendations: Number of recommendations to return
            
        Returns:
            List of enhanced recommendation dictionaries
        """
        print(f"\n🔍 Processing recommendations for user preferences...")
        print(f"Budget: ${user_preferences['budget']}/day")
        print(f"Duration: {user_preferences['duration']} days")
        print(f"Trip Type: {user_preferences['trip_type']}")
        print(f"Season: {user_preferences['season']}")
        
        # Step 1: Get ML-driven recommendations (CORE DECISION LAYER)
        print(f"\n🧠 ML Engine: Generating recommendations...")
        user_profile = self.ml_engine.preprocessor.create_user_profile_features(
            budget=user_preferences['budget'],
            duration=user_preferences['duration'],
            trip_type=user_preferences['trip_type'],
            season=user_preferences['season']
        )
        
        ml_recommendations = self.ml_engine.get_recommendations(
            user_profile, top_n=num_recommendations
        )
        
        if not ml_recommendations:
            print("❌ No ML recommendations found for these preferences")
            return []
        
        print(f"✅ ML Engine found {len(ml_recommendations)} recommendations")
        
        # Step 2: Enhance each recommendation with LLM content
        enhanced_recommendations = []
        
        for i, ml_rec in enumerate(ml_recommendations, 1):
            print(f"\n🤖 LLM Engine: Enhancing recommendation {i}/{len(ml_recommendations)}")
            print(f"   Destination: {ml_rec['destination']}")
            
            # Generate comprehensive itinerary using LLM + APIs
            itinerary = self.llm_engine.generate_itinerary(
                destination_data=ml_rec,
                user_preferences=user_preferences,
                duration=user_preferences['duration']
            )
            
            # Combine ML recommendation with LLM enhancement
            enhanced_rec = {
                # Core ML data (decision layer)
                "ml_recommendation": {
                    "destination": ml_rec['destination'],
                    "country": ml_rec['country'],
                    "region": ml_rec['region'],
                    "overall_score": ml_rec['overall_score'],
                    "cost_per_day": ml_rec['cost_per_day'],
                    "trip_type": ml_rec['trip_type'],
                    "duration_range": ml_rec['duration_range'],
                    "ml_explanation": ml_rec['explanation']
                },
                
                # LLM-generated content (presentation layer)
                "llm_enhancement": {
                    "personalized_itinerary": itinerary['daily_itinerary'],
                    "natural_explanation": itinerary['recommendation_explanation'],
                    "travel_tips": itinerary['travel_tips']
                },
                
                # API-enriched data (real-world context)
                "real_world_data": {
                    "weather_info": itinerary['weather_info'],
                    "top_attractions": itinerary['top_attractions'],
                    "estimated_total_cost": itinerary['total_estimated_cost']
                },
                
                # Metadata
                "generation_info": {
                    "ml_engine_version": "TripX v1.0",
                    "llm_provider": self.llm_engine.llm_provider,
                    "generated_at": itinerary['generated_at']
                }
            }
            
            enhanced_recommendations.append(enhanced_rec)
            print(f"   ✅ Enhancement complete")
        
        print(f"\n🎉 Generated {len(enhanced_recommendations)} enhanced recommendations")
        return enhanced_recommendations
    
    def generate_comparison_report(self, recommendations: List[Dict]) -> str:
        """
        Generate LLM-powered comparison report for multiple recommendations.
        
        Args:
            recommendations: List of enhanced recommendations
            
        Returns:
            Natural language comparison report
        """
        if not recommendations:
            return "No recommendations available for comparison."
        
        # Extract key data for comparison
        comparison_data = []
        for rec in recommendations:
            ml_data = rec['ml_recommendation']
            comparison_data.append({
                "destination": ml_data['destination'],
                "score": ml_data['overall_score'],
                "cost": ml_data['cost_per_day'],
                "type": ml_data['trip_type']
            })
        
        # Generate comparison prompt
        prompt = f"""Compare these {len(comparison_data)} travel destinations and explain the key differences:

"""
        for i, dest in enumerate(comparison_data, 1):
            prompt += f"{i}. {dest['destination']}: Score {dest['score']:.3f}, ${dest['cost']}/day, {dest['type']} travel\n"
        
        prompt += "\nProvide a clear comparison highlighting strengths of each destination and help the user choose."
        
        comparison_text = self.llm_engine.generate_llm_text(prompt, max_tokens=400)
        
        if not comparison_text or len(comparison_text) < 50:
            # Fallback comparison
            comparison_text = f"""Here's a comparison of your top {len(comparison_data)} recommendations:

{comparison_data[0]['destination']} leads with the highest recommendation score of {comparison_data[0]['score']:.3f}, offering {comparison_data[0]['type']} experiences at ${comparison_data[0]['cost']}/day.

Each destination has been selected based on your preferences and offers unique advantages. Consider your priorities: budget, experience type, and personal interests when making your final choice."""
        
        return comparison_text
    
    def explain_ml_llm_separation(self) -> Dict[str, str]:
        """
        Explain the architectural decision to separate ML and LLM concerns.
        
        Returns:
            Dictionary explaining the separation rationale
        """
        return {
            "architecture_principle": "Clear separation of ML decision-making and LLM text generation",
            
            "ml_engine_role": "Makes data-driven recommendations using feature engineering, similarity scoring, and ranking algorithms. Provides objective, consistent decisions based on user preferences and destination characteristics.",
            
            "llm_engine_role": "Generates human-readable explanations, itineraries, and travel tips. Enhances user experience without influencing core recommendation logic.",
            
            "why_separate": "Prevents LLM hallucinations from affecting recommendation quality. Ensures recommendations are based on data and ML algorithms, not language model biases. Allows independent testing and optimization of each component.",
            
            "api_integration": "External APIs provide real-world context (weather, attractions) without changing core recommendations. Enriches user experience with current, relevant information.",
            
            "benefits": "Reliable recommendations + engaging presentation + real-world context. Each component can be improved independently. Clear debugging and testing boundaries."
        }


def test_integrated_system():
    """
    Test the integrated ML + LLM system with sample user profiles.
    """
    print("🧪 Testing TripX Integrated ML + LLM System")
    print("=" * 60)
    
    # Initialize integrated engine
    engine = TripXIntegratedEngine(
        data_path='data/raw/dest.csv',
        llm_provider='local'  # Will fallback to templates if local LLM unavailable
    )
    
    # Test with two different user profiles
    test_profiles = [
        {
            "name": "Cultural Explorer",
            "budget": 80,
            "duration": 6,
            "trip_type": "culture",
            "season": "spring"
        },
        {
            "name": "Beach Relaxer",
            "budget": 120,
            "duration": 8,
            "trip_type": "beach",
            "season": "summer"
        }
    ]
    
    all_results = {}
    
    for profile in test_profiles:
        print(f"\n{'='*60}")
        print(f"🎭 TESTING PROFILE: {profile['name']}")
        print(f"{'='*60}")
        
        # Get enhanced recommendations
        recommendations = engine.get_enhanced_recommendations(
            user_preferences=profile,
            num_recommendations=2
        )
        
        if recommendations:
            print(f"\n📊 RESULTS FOR {profile['name']}:")
            
            for i, rec in enumerate(recommendations, 1):
                ml_data = rec['ml_recommendation']
                llm_data = rec['llm_enhancement']
                api_data = rec['real_world_data']
                
                print(f"\n--- Recommendation {i}: {ml_data['destination']} ---")
                print(f"🎯 ML Score: {ml_data['overall_score']:.3f}")
                print(f"💰 Cost: ${ml_data['cost_per_day']}/day")
                print(f"🌍 Region: {ml_data['region']}")
                
                print(f"\n🧠 ML Explanation:")
                print(f"   {ml_data['ml_explanation']}")
                
                print(f"\n🤖 LLM Natural Explanation:")
                print(f"   {llm_data['natural_explanation'][:200]}...")
                
                print(f"\n📋 Sample Itinerary:")
                itinerary_preview = llm_data['personalized_itinerary'][:300]
                print(f"   {itinerary_preview}...")
                
                print(f"\n🌤️ Weather: {api_data['weather_info']['weather_note']}")
                print(f"🏛️ Top Attraction: {api_data['top_attractions'][0]['name']}")
                
                print(f"\n💡 Travel Tips:")
                for tip in llm_data['travel_tips'][:2]:
                    print(f"   • {tip}")
            
            # Generate comparison report
            print(f"\n📈 COMPARISON REPORT:")
            comparison = engine.generate_comparison_report(recommendations)
            print(f"   {comparison}")
            
        else:
            print(f"❌ No recommendations found for {profile['name']}")
        
        all_results[profile['name']] = recommendations
    
    # Explain architecture
    print(f"\n{'='*60}")
    print(f"🏗️ ARCHITECTURE EXPLANATION")
    print(f"{'='*60}")
    
    architecture = engine.explain_ml_llm_separation()
    for key, value in architecture.items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(f"   {value}")
    
    print(f"\n✅ INTEGRATED SYSTEM TEST COMPLETE")
    print(f"🎯 ML Engine: Reliable data-driven recommendations")
    print(f"🤖 LLM Engine: Natural language enhancement")
    print(f"🌐 API Layer: Real-world context enrichment")
    
    return all_results


if __name__ == "__main__":
    # Run comprehensive test
    test_results = test_integrated_system()
    
    # Save results for analysis
    with open("integrated_test_results.json", "w") as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n📄 Test results saved to 'integrated_test_results.json'")
    print(f"🚀 Ready for Day 7 UI implementation!")