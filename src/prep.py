import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class TripXPreprocessor:
    
    def __init__(self):
        self.cost_categories = {
            'budget': (0, 60),
            'mid': (60, 120), 
            'premium': (120, 200),
            'luxury': (200, float('inf'))
        }
        
        self.trip_types = ['beach', 'culture', 'urban', 'luxury', 'nature']
        self.seasons = ['spring', 'summer', 'fall', 'winter', 'dry_season', 'cool_season']
        
        self.quality_weights = {
            'popularity': 0.6,
            'safety': 0.4
        }
    
    def categorize_cost(self, cost: float) -> str:
        for category, (min_cost, max_cost) in self.cost_categories.items():
            if min_cost <= cost < max_cost:
                return category
        return 'luxury'
    
    def calculate_duration_compatibility(self, user_days: int, min_days: int, max_days: int) -> float:
        if min_days <= user_days <= max_days:
            return 1.0
        
        if user_days < min_days:
            distance = min_days - user_days
        else:
            distance = user_days - max_days
        
        if distance == 1:
            return 0.8
        elif distance <= 3:
            return 0.5
        else:
            return 0.2
    
    def calculate_season_match(self, user_season: str, dest_season: str) -> float:
        if user_season == dest_season:
            return 1.0
        
        season_similarity = {
            'spring': ['summer', 'fall'],
            'summer': ['spring', 'dry_season'],
            'fall': ['spring', 'winter'],
            'winter': ['fall', 'cool_season'],
            'dry_season': ['summer', 'spring'],
            'cool_season': ['winter', 'fall']
        }
        
        if dest_season in season_similarity.get(user_season, []):
            return 0.6
        
        return 0.3
    
    def calculate_quality_score(self, popularity: float, safety: float) -> float:
        return (popularity * self.quality_weights['popularity'] + 
                safety * self.quality_weights['safety'])
    
    def encode_trip_type(self, trip_type: str) -> Dict[str, int]:
        encoding = {f'type_{t}': 0 for t in self.trip_types}
        if trip_type in self.trip_types:
            encoding[f'type_{trip_type}'] = 1
        return encoding
    
    def normalize_numerical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df_normalized = df.copy()
        
        numerical_features = ['avg_cost_per_day', 'popularity_score', 'safety_score', 
                            'quality_score', 'min_days', 'max_days']
        
        for feature in numerical_features:
            if feature in df_normalized.columns:
                min_val = df_normalized[feature].min()
                max_val = df_normalized[feature].max()
                df_normalized[f'{feature}_norm'] = (df_normalized[feature] - min_val) / (max_val - min_val)
        
        return df_normalized
    
    def preprocess_destinations(self, df: pd.DataFrame) -> pd.DataFrame:
        processed_df = df.copy()
        
        processed_df['cost_category'] = processed_df['avg_cost_per_day'].apply(self.categorize_cost)
        
        processed_df['quality_score'] = processed_df.apply(
            lambda row: self.calculate_quality_score(row['popularity_score'], row['safety_score']), 
            axis=1
        )
        
        trip_type_encoded = processed_df['trip_type'].apply(self.encode_trip_type)
        trip_type_df = pd.DataFrame(trip_type_encoded.tolist(), index=processed_df.index)
        processed_df = pd.concat([processed_df, trip_type_df], axis=1)
        
        processed_df['duration_range'] = processed_df['max_days'] - processed_df['min_days']
        processed_df['duration_flexibility'] = processed_df['duration_range'] / processed_df['max_days']
        
        processed_df = self.normalize_numerical_features(processed_df)
        
        return processed_df
    
    def create_user_profile_features(self, budget: float, duration: int, 
                                   trip_type: str, season: str) -> Dict:
        user_features = {
            'budget': budget,
            'duration': duration,
            'cost_category': self.categorize_cost(budget),
            'preferred_season': season,
            'preferred_trip_type': trip_type
        }
        
        trip_encoding = self.encode_trip_type(trip_type)
        user_features.update(trip_encoding)
        
        return user_features


def load_and_preprocess_data(data_path: str = '../data/raw/dest.csv') -> Tuple[pd.DataFrame, TripXPreprocessor]:
    df = pd.read_csv(data_path)
    preprocessor = TripXPreprocessor()
    processed_df = preprocessor.preprocess_destinations(df)
    
    print(f"Preprocessing complete!")
    print(f"Original features: {df.shape[1]}")
    print(f"Engineered features: {processed_df.shape[1]}")
    print(f"New features added: {processed_df.shape[1] - df.shape[1]}")
    
    return processed_df, preprocessor


if __name__ == "__main__":
    df, preprocessor = load_and_preprocess_data()
    
    print("\n=== SAMPLE PROCESSED FEATURES ===")
    feature_cols = ['destination', 'cost_category', 'quality_score', 'duration_flexibility', 
                   'type_culture', 'type_beach', 'avg_cost_per_day_norm']
    print(df[feature_cols].head())
    
    print("\n=== SAMPLE USER PROFILE ===")
    user_profile = preprocessor.create_user_profile_features(
        budget=100, duration=5, trip_type='culture', season='spring'
    )
    for key, value in user_profile.items():
        print(f"{key}: {value}")