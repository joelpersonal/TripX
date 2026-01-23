import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from recsys import create_recommendation_engine

def run_demo():
    print("TripX - Find Your Perfect Trip")
    print("=" * 45)
    
    engine, df = create_recommendation_engine('data/raw/dest.csv')
    print(f"Loaded {len(df)} destinations from around the world\n")
    
    demo_users = [
        {
            "name": "Sarah - Digital Nomad",
            "budget": 60,
            "duration": 14,
            "trip_type": "culture",
            "season": "spring"
        },
        {
            "name": "Mike - Adventure Seeker", 
            "budget": 100,
            "duration": 10,
            "trip_type": "nature",
            "season": "summer"
        },
        {
            "name": "Emma - Luxury Escape",
            "budget": 200,
            "duration": 6,
            "trip_type": "beach",
            "season": "winter"
        }
    ]
    
    for user_info in demo_users:
        print(f"\n {user_info['name']}")
        print(f"Budget: ${user_info['budget']}/day | {user_info['duration']} days | {user_info['trip_type']} | {user_info['season']}")
        print("-" * 50)
        
        user_profile = engine.preprocessor.create_user_profile_features(
            budget=user_info['budget'],
            duration=user_info['duration'],
            trip_type=user_info['trip_type'],
            season=user_info['season']
        )
        
        recommendations = engine.get_recommendations(user_profile, top_n=2)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['destination']}, {rec['country']}")
            print(f"   💰 ${rec['cost_per_day']}/day | ⭐ {rec['overall_score']:.3f}")
            print(f"   💡 {rec['explanation']}")

if __name__ == "__main__":
    run_demo()