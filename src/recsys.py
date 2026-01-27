import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from prep import TripXPreprocessor


class TripXRecommendationEngine:
    
    def __init__(self, processed_df: pd.DataFrame, preprocessor: TripXPreprocessor):
        self.df = processed_df
        self.preprocessor = preprocessor
        
        # Scoring weights for different factors
        self.scoring_weights = {
            'budget_fit': 0.3,
            'duration_fit': 0.2,
            'trip_type_match': 0.25,
            'season_match': 0.15,
            'quality_bonus': 0.1
        }
    
    def calculate_budget_fit_score(self, user_budget: float, dest_cost: float) -> float:
        # Perfect fit if destination is within budget
        if user_budget >= dest_cost:
            return 1.0
        
        # Partial scores for slightly over budget
        budget_ratio = dest_cost / user_budget
        if budget_ratio <= 1.2:
            return 0.8
        elif budget_ratio <= 1.5:
            return 0.5
        else:
            return 0.1
    
    def calculate_trip_type_score(self, user_profile: Dict, destination_row: pd.Series) -> float:
        user_trip_type = user_profile['preferred_trip_type']
        dest_trip_type = destination_row['trip_type']
        
        # Exact match gets full score
        if user_trip_type == dest_trip_type:
            return 1.0
        
        # Compatible types get partial score
        type_compatibility = {
            'culture': ['urban', 'nature'],
            'beach': ['nature', 'luxury'],
            'urban': ['culture', 'luxury'],
            'luxury': ['beach', 'urban'],
            'nature': ['beach', 'culture']
        }
        
        if dest_trip_type in type_compatibility.get(user_trip_type, []):
            return 0.6
        
        return 0.2
    
    def calculate_overall_score(self, user_profile: Dict, destination_row: pd.Series) -> Tuple[float, Dict]:
        budget_score = self.calculate_budget_fit_score(
            user_profile['budget'], destination_row['avg_cost_per_day']
        )
        
        duration_score = self.preprocessor.calculate_duration_compatibility(
            user_profile['duration'], destination_row['min_days'], destination_row['max_days']
        )
        
        trip_type_score = self.calculate_trip_type_score(user_profile, destination_row)
        
        season_score = self.preprocessor.calculate_season_match(
            user_profile['preferred_season'], destination_row['season_best']
        )
        
        quality_score = destination_row['quality_score_norm']
        
        total_score = (
            self.scoring_weights['budget_fit'] * budget_score +
            self.scoring_weights['duration_fit'] * duration_score +
            self.scoring_weights['trip_type_match'] * trip_type_score +
            self.scoring_weights['season_match'] * season_score +
            self.scoring_weights['quality_bonus'] * quality_score
        )
        
        score_breakdown = {
            'budget_fit': budget_score,
            'duration_fit': duration_score,
            'trip_type_match': trip_type_score,
            'season_match': season_score,
            'quality_bonus': quality_score,
            'total_score': total_score
        }
        
        return total_score, score_breakdown
    
    def filter_destinations(self, user_profile: Dict) -> pd.DataFrame:
        filtered_df = self.df.copy()
        
        # Filter by budget (allow some flexibility)
        max_budget = user_profile['budget'] * 1.3
        filtered_df = filtered_df[filtered_df['avg_cost_per_day'] <= max_budget]
        
        # Filter by duration compatibility
        user_duration = user_profile['duration']
        duration_compatible = filtered_df.apply(
            lambda row: self.preprocessor.calculate_duration_compatibility(
                user_duration, row['min_days'], row['max_days']
            ) >= 0.2, axis=1
        )
        filtered_df = filtered_df[duration_compatible]
        
        return filtered_df
    
    def generate_explanation(self, destination_row: pd.Series, score_breakdown: Dict, 
                           user_profile: Dict) -> str:
        dest_name = destination_row['destination']
        cost = destination_row['avg_cost_per_day']
        user_budget = user_profile['budget']
        
        explanations = []
        
        if score_breakdown['budget_fit'] >= 0.8:
            if cost <= user_budget:
                explanations.append(f"Great value at ${cost}/day (within your ${user_budget} budget)")
            else:
                explanations.append(f"Slightly over budget at ${cost}/day but worth it")
        elif score_breakdown['budget_fit'] >= 0.5:
            explanations.append(f"Moderate fit for ${user_budget} budget (${cost}/day)")
        
        if score_breakdown['trip_type_match'] >= 0.8:
            explanations.append(f"Perfect match for {user_profile['preferred_trip_type']} travel")
        elif score_breakdown['trip_type_match'] >= 0.5:
            explanations.append(f"Great alternative to {user_profile['preferred_trip_type']} travel")
        
        if score_breakdown['duration_fit'] >= 0.8:
            explanations.append(f"Ideal for your {user_profile['duration']}-day trip")
        elif score_breakdown['duration_fit'] >= 0.5:
            explanations.append(f"Works for {user_profile['duration']} days")
        
        if score_breakdown['season_match'] >= 0.8:
            explanations.append(f"Perfect timing for {user_profile['preferred_season']} travel")
        elif score_breakdown['season_match'] >= 0.5:
            explanations.append(f"Good season for travel")
        
        if destination_row['quality_score'] >= 8.5:
            explanations.append(f"High quality destination (popularity: {destination_row['popularity_score']:.1f}, safety: {destination_row['safety_score']:.1f})")
        elif destination_row['quality_score'] >= 7.5:
            explanations.append(f"Well-rated destination")
        
        return " • ".join(explanations)
    
    def get_recommendations(self, user_profile: Dict, top_n: int = 5) -> List[Dict]:
        filtered_destinations = self.filter_destinations(user_profile)
        
        if filtered_destinations.empty:
            return []
        
        recommendations = []
        
        for idx, row in filtered_destinations.iterrows():
            total_score, score_breakdown = self.calculate_overall_score(user_profile, row)
            
            explanation = self.generate_explanation(row, score_breakdown, user_profile)
            
            recommendation = {
                'destination': row['destination'],
                'country': row['country'],
                'region': row['region'],
                'cost_per_day': row['avg_cost_per_day'],
                'trip_type': row['trip_type'],
                'duration_range': f"{row['min_days']}-{row['max_days']} days",
                'best_season': row['season_best'],
                'popularity_score': row['popularity_score'],
                'safety_score': row['safety_score'],
                'overall_score': round(total_score, 3),
                'explanation': explanation,
                'score_breakdown': score_breakdown
            }
            
            recommendations.append(recommendation)
        
        recommendations.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def explain_no_results(self, user_profile: Dict) -> str:
        explanations = []
        
        budget_destinations = self.df[self.df['avg_cost_per_day'] <= user_profile['budget'] * 1.3]
        if budget_destinations.empty:
            min_cost = self.df['avg_cost_per_day'].min()
            explanations.append(f"Budget too low - minimum destination cost is ${min_cost}/day")
        
        user_duration = user_profile['duration']
        duration_compatible = self.df.apply(
            lambda row: self.preprocessor.calculate_duration_compatibility(
                user_duration, row['min_days'], row['max_days']
            ) >= 0.2, axis=1
        )
        
        if not duration_compatible.any():
            explanations.append(f"No destinations suitable for {user_duration}-day trips")
        
        if not explanations:
            explanations.append("Try adjusting your preferences for more options")
        
        return " • ".join(explanations)


def create_recommendation_engine(data_path: str = '../data/raw/dest.csv'):
    from prep import load_and_preprocess_data
    
    processed_df, preprocessor = load_and_preprocess_data(data_path)
    engine = TripXRecommendationEngine(processed_df, preprocessor)
    
    return engine, processed_df


if __name__ == "__main__":
    engine, df = create_recommendation_engine()
    
    test_profiles = [
        {
            "name": "Budget Backpacker",
            "budget": 50,
            "duration": 10,
            "trip_type": "culture",
            "season": "spring"
        },
        {
            "name": "Luxury Traveler", 
            "budget": 200,
            "duration": 5,
            "trip_type": "luxury",
            "season": "winter"
        },
        {
            "name": "Beach Lover",
            "budget": 80,
            "duration": 7,
            "trip_type": "beach",
            "season": "summer"
        }
    ]
    
    for profile_info in test_profiles:
        print(f"\n{'='*50}")
        print(f"RECOMMENDATIONS FOR: {profile_info['name']}")
        print(f"Budget: ${profile_info['budget']}/day | Duration: {profile_info['duration']} days")
        print(f"Preferences: {profile_info['trip_type']} travel in {profile_info['season']}")
        print(f"{'='*50}")
        
        user_profile = engine.preprocessor.create_user_profile_features(
            budget=profile_info['budget'],
            duration=profile_info['duration'],
            trip_type=profile_info['trip_type'],
            season=profile_info['season']
        )
        
        recommendations = engine.get_recommendations(user_profile, top_n=3)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['destination']}, {rec['country']}")
                print(f"   Cost: ${rec['cost_per_day']}/day | {rec['duration_range']} | {rec['trip_type']}")
                print(f"   Score: {rec['overall_score']:.3f}")
                print(f"   Why: {rec['explanation']}")
        else:
            print(f"\nNo recommendations found.")
            print(f"Reason: {engine.explain_no_results(user_profile)}")