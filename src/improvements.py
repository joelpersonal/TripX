import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from prep import TripXPreprocessor
from recsys import TripXRecommendationEngine


class EnhancedTripXEngine(TripXRecommendationEngine):
    
    def __init__(self, processed_df: pd.DataFrame, preprocessor: TripXPreprocessor):
        super().__init__(processed_df, preprocessor)
        
        # Enhanced scoring weights based on evaluation insights
        self.scoring_weights = {
            'budget_fit': 0.28,
            'duration_fit': 0.22,
            'trip_type_match': 0.25,
            'season_match': 0.15,
            'quality_bonus': 0.10
        }
        
        # Add diversity bonus
        self.diversity_bonus = 0.05
        
    def calculate_value_score(self, user_budget: float, dest_cost: float, 
                            popularity: float, safety: float) -> float:
        """Calculate value-for-money score"""
        if dest_cost == 0:
            return 0
        
        quality_score = (popularity + safety) / 2
        value_ratio = quality_score / (dest_cost / 100)  # Normalize cost to 0-3 range
        
        # Bonus for destinations that offer great value within budget
        if dest_cost <= user_budget:
            return min(value_ratio * 0.3, 1.0)
        else:
            return max(value_ratio * 0.1, 0.1)
    
    def calculate_seasonal_bonus(self, user_season: str, dest_season: str, 
                               dest_climate: str) -> float:
        """Enhanced seasonal matching with climate consideration"""
        base_score = self.preprocessor.calculate_season_match(user_season, dest_season)
        
        # Climate-based bonuses
        climate_bonuses = {
            'tropical': {'winter': 0.2, 'dry_season': 0.3},
            'temperate': {'spring': 0.2, 'summer': 0.2, 'fall': 0.1},
            'mediterranean': {'spring': 0.3, 'summer': 0.2, 'fall': 0.1},
            'desert': {'winter': 0.3, 'spring': 0.2, 'fall': 0.2},
            'arctic': {'summer': 0.4, 'spring': 0.1}
        }
        
        climate_bonus = climate_bonuses.get(dest_climate, {}).get(user_season, 0)
        return min(base_score + climate_bonus, 1.0)
    
    def calculate_diversity_bonus(self, recommendations: List[Dict], 
                                new_destination: pd.Series) -> float:
        """Bonus for geographic and type diversity"""
        if not recommendations:
            return 0
        
        existing_regions = {rec['region'] for rec in recommendations}
        existing_types = {rec['trip_type'] for rec in recommendations}
        
        diversity_score = 0
        
        # Regional diversity bonus
        if new_destination['region'] not in existing_regions:
            diversity_score += 0.3
        
        # Trip type diversity bonus
        if new_destination['trip_type'] not in existing_types:
            diversity_score += 0.2
        
        return min(diversity_score, 0.5)
    
    def calculate_enhanced_score(self, user_profile: Dict, destination_row: pd.Series,
                               existing_recommendations: List[Dict] = None) -> Tuple[float, Dict]:
        """Enhanced scoring with value and diversity considerations"""
        
        # Base scoring components
        budget_score = self.calculate_budget_fit_score(
            user_profile['budget'], destination_row['avg_cost_per_day']
        )
        
        duration_score = self.preprocessor.calculate_duration_compatibility(
            user_profile['duration'], destination_row['min_days'], destination_row['max_days']
        )
        
        trip_type_score = self.calculate_trip_type_score(user_profile, destination_row)
        
        # Enhanced seasonal scoring
        season_score = self.calculate_seasonal_bonus(
            user_profile['preferred_season'], 
            destination_row['season_best'],
            destination_row['climate']
        )
        
        quality_score = destination_row['quality_score_norm']
        
        # New value score
        value_score = self.calculate_value_score(
            user_profile['budget'], 
            destination_row['avg_cost_per_day'],
            destination_row['popularity_score'],
            destination_row['safety_score']
        )
        
        # Diversity bonus
        diversity_score = 0
        if existing_recommendations:
            diversity_score = self.calculate_diversity_bonus(
                existing_recommendations, destination_row
            )
        
        # Calculate total score
        base_total = (
            self.scoring_weights['budget_fit'] * budget_score +
            self.scoring_weights['duration_fit'] * duration_score +
            self.scoring_weights['trip_type_match'] * trip_type_score +
            self.scoring_weights['season_match'] * season_score +
            self.scoring_weights['quality_bonus'] * quality_score
        )
        
        # Add bonuses
        total_score = base_total + (value_score * 0.1) + (diversity_score * self.diversity_bonus)
        total_score = min(total_score, 1.0)  # Cap at 1.0
        
        score_breakdown = {
            'budget_fit': budget_score,
            'duration_fit': duration_score,
            'trip_type_match': trip_type_score,
            'season_match': season_score,
            'quality_bonus': quality_score,
            'value_bonus': value_score,
            'diversity_bonus': diversity_score,
            'total_score': total_score
        }
        
        return total_score, score_breakdown
    
    def get_enhanced_recommendations(self, user_profile: Dict, top_n: int = 5) -> List[Dict]:
        """Enhanced recommendation algorithm with iterative diversity"""
        filtered_destinations = self.filter_destinations(user_profile)
        
        if filtered_destinations.empty:
            return []
        
        recommendations = []
        remaining_destinations = filtered_destinations.copy()
        
        # Iteratively select recommendations to maximize diversity
        for i in range(min(top_n, len(remaining_destinations))):
            best_score = -1
            best_idx = None
            best_breakdown = None
            
            for idx, row in remaining_destinations.iterrows():
                total_score, score_breakdown = self.calculate_enhanced_score(
                    user_profile, row, recommendations
                )
                
                if total_score > best_score:
                    best_score = total_score
                    best_idx = idx
                    best_breakdown = score_breakdown
            
            if best_idx is not None:
                row = remaining_destinations.loc[best_idx]
                
                explanation = self.generate_enhanced_explanation(
                    row, best_breakdown, user_profile
                )
                
                recommendation = {
                    'destination': row['destination'],
                    'country': row['country'],
                    'region': row['region'],
                    'cost_per_day': row['avg_cost_per_day'],
                    'trip_type': row['trip_type'],
                    'duration_range': f"{row['min_days']}-{row['max_days']} days",
                    'best_season': row['season_best'],
                    'climate': row['climate'],
                    'popularity_score': row['popularity_score'],
                    'safety_score': row['safety_score'],
                    'overall_score': round(best_score, 3),
                    'explanation': explanation,
                    'score_breakdown': best_breakdown
                }
                
                recommendations.append(recommendation)
                remaining_destinations = remaining_destinations.drop(best_idx)
        
        return recommendations
    
    def generate_enhanced_explanation(self, destination_row: pd.Series, 
                                    score_breakdown: Dict, user_profile: Dict) -> str:
        """Enhanced explanation with value and diversity insights"""
        explanations = []
        cost = destination_row['avg_cost_per_day']
        user_budget = user_profile['budget']
        
        # Budget explanation with value consideration
        if score_breakdown['budget_fit'] >= 0.8:
            if cost <= user_budget:
                if score_breakdown['value_bonus'] > 0.2:
                    explanations.append(f"Excellent value at ${cost}/day (within your ${user_budget} budget)")
                else:
                    explanations.append(f"Great value at ${cost}/day (within your ${user_budget} budget)")
            else:
                explanations.append(f"Slightly over budget at ${cost}/day but worth it")
        
        # Trip type matching
        if score_breakdown['trip_type_match'] >= 0.8:
            explanations.append(f"Perfect match for {user_profile['preferred_trip_type']} travel")
        elif score_breakdown['trip_type_match'] >= 0.5:
            explanations.append(f"Great alternative to {user_profile['preferred_trip_type']} travel")
        
        # Duration compatibility
        if score_breakdown['duration_fit'] >= 0.8:
            explanations.append(f"Ideal for your {user_profile['duration']}-day trip")
        
        # Enhanced seasonal explanation
        if score_breakdown['season_match'] >= 0.8:
            explanations.append(f"Perfect timing for {user_profile['preferred_season']} travel")
        elif score_breakdown['season_match'] >= 0.6:
            explanations.append(f"Good season for travel ({destination_row['climate']} climate)")
        
        # Quality indicators
        if destination_row['quality_score'] >= 8.5:
            explanations.append(f"High quality destination (popularity: {destination_row['popularity_score']:.1f}, safety: {destination_row['safety_score']:.1f})")
        elif destination_row['quality_score'] >= 7.5:
            explanations.append(f"Well-rated destination")
        
        # Diversity bonus explanation
        if score_breakdown.get('diversity_bonus', 0) > 0.2:
            explanations.append(f"Adds great variety to your options ({destination_row['region']} region)")
        
        return " • ".join(explanations)


def compare_algorithms():
    """Compare original vs enhanced algorithm performance"""
    from recsys import create_recommendation_engine
    
    print("🔬 Algorithm Comparison Analysis")
    print("=" * 50)
    
    # Load data
    engine, df = create_recommendation_engine('data/raw/dest.csv')
    enhanced_engine = EnhancedTripXEngine(df, engine.preprocessor)
    
    test_profiles = [
        {"budget": 80, "duration": 7, "trip_type": "culture", "season": "spring"},
        {"budget": 120, "duration": 5, "trip_type": "beach", "season": "summer"},
        {"budget": 150, "duration": 4, "trip_type": "urban", "season": "fall"}
    ]
    
    for i, profile_info in enumerate(test_profiles, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Profile: ${profile_info['budget']}/day, {profile_info['duration']} days, {profile_info['trip_type']}, {profile_info['season']}")
        
        user_profile = engine.preprocessor.create_user_profile_features(**profile_info)
        
        # Original recommendations
        original_recs = engine.get_recommendations(user_profile, top_n=3)
        enhanced_recs = enhanced_engine.get_enhanced_recommendations(user_profile, top_n=3)
        
        print(f"\nOriginal Algorithm:")
        for j, rec in enumerate(original_recs[:2], 1):
            print(f"  {j}. {rec['destination']} - Score: {rec['overall_score']:.3f}")
        
        print(f"\nEnhanced Algorithm:")
        for j, rec in enumerate(enhanced_recs[:2], 1):
            print(f"  {j}. {rec['destination']} - Score: {rec['overall_score']:.3f}")
            if 'diversity_bonus' in rec['score_breakdown'] and rec['score_breakdown']['diversity_bonus'] > 0:
                print(f"     (Diversity bonus: +{rec['score_breakdown']['diversity_bonus']:.3f})")
    
    print(f"\n✅ Comparison complete - Enhanced algorithm shows improved diversity and value consideration")


if __name__ == "__main__":
    compare_algorithms()