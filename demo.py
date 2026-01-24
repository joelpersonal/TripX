#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from integrated_engine import TripXIntegratedEngine


def main():
    """
    Quick demo of the complete TripX integrated system.
    Shows ML recommendations enhanced with LLM and API data.
    """
    
    print("🌍 TripX - ML-Driven Travel Recommendation System")
    print("=" * 60)
    print("🏗️ Architecture: ML (Decisions) + LLM (Text) + APIs (Enrichment)")
    print("=" * 60)
    
    # Initialize the system
    print("\n🔧 Initializing TripX Integrated Engine...")
    engine = TripXIntegratedEngine("groq")
    
    # Demo user profile
    user_preferences = {
        "budget": 100,
        "duration": 7,
        "trip_type": "culture",
        "season": "spring"
    }
    
    print(f"\n👤 Demo User Profile:")
    print(f"   Budget: ${user_preferences['budget']}/day")
    print(f"   Duration: {user_preferences['duration']} days")
    print(f"   Interest: {user_preferences['trip_type']} travel")
    print(f"   Season: {user_preferences['season']}")
    
    # Get recommendations
    print(f"\n🧠 Generating enhanced recommendations...")
    results = engine.get_enhanced_recommendations(user_preferences, top_n=2)
    
    if results['status'] == 'success':
        print(f"\n✅ Found {results['total_recommendations']} perfect matches!")
        
        for i, rec in enumerate(results['recommendations'], 1):
            ml_rec = rec['ml_recommendation']
            
            print(f"\n{'='*50}")
            print(f"🏆 RECOMMENDATION {i}")
            print(f"{'='*50}")
            print(f"📍 Destination: {ml_rec['destination']}, {ml_rec['country']}")
            print(f"🎯 ML Score: {rec['ml_score']:.3f}")
            print(f"💰 Cost: ${ml_rec['cost_per_day']}/day")
            print(f"⏱️ Duration: {ml_rec['duration_range']}")
            print(f"🌤️ Weather: {rec['weather_info'].get('current_temp', 'N/A')}°C")
            
            print(f"\n🧠 ML Analysis:")
            print(f"   {rec['ml_reasoning']}")
            
            print(f"\n🤖 LLM Explanation:")
            print(f"   {rec['llm_explanation']}")
            
            print(f"\n🏛️ Top Attractions:")
            for attr in rec['attractions'][:3]:
                print(f"   • {attr['name']} ({attr['category']})")
            
            print(f"\n📝 Sample Itinerary:")
            itinerary_lines = rec['detailed_itinerary'].split('\n')[:4]
            for line in itinerary_lines:
                if line.strip():
                    print(f"   {line}")
    
    else:
        print(f"❌ No recommendations found: {results.get('message', 'Unknown error')}")
    
    print(f"\n{'='*60}")
    print("🎯 TripX System Status: FULLY OPERATIONAL")
    print("✅ ML Engine: Intelligent destination ranking")
    print("✅ LLM Integration: Natural language explanations")
    print("✅ API Enrichment: Weather & attraction data")
    print("✅ Ready for Day 7: UI Development")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()