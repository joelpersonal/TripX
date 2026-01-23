# TripX - Travel Recommendation System

A machine learning-based travel recommendation system that helps users find destinations matching their preferences and budget. Built with Python and focused on explainable recommendations.

## What it does

TripX analyzes travel destinations and recommends the best matches based on:
- Budget constraints
- Trip duration preferences  
- Travel style (beach, culture, urban, etc.)
- Seasonal timing
- Safety and popularity factors

The system provides clear explanations for why each destination was recommended, making it easy to understand the reasoning behind suggestions.

## Project Structure
```
TripX/
├── data/raw/dest.csv                    # Destination dataset (60 destinations)
├── notebooks/                           # Analysis notebooks
│   ├── 01_overview.ipynb               # Data exploration
│   ├── 02_eda.ipynb                    # Feature analysis
│   ├── 03_feature_engineering.ipynb    # Feature engineering
│   └── 04_recommendation_testing.ipynb # Algorithm testing
├── src/
│   ├── prep.py                         # Data preprocessing
│   └── recsys.py                       # Recommendation engine
├── demo.py                             # Quick demo script
├── app.py                              # Streamlit interface
└── requirements.txt
```

## Dataset

The system uses a curated dataset of 60 popular travel destinations with features like:
- Cost per day ($25-300 range)
- Optimal trip duration
- Best travel seasons
- Trip types and activities
- Safety and popularity scores

## Technical Approach

**Data Processing**: Cost categorization, duration compatibility scoring, quality indicators
**ML Strategy**: Multi-stage filtering and similarity-based ranking
**Features**: Engineered features for budget matching, preference scoring, and quality ranking

## Development Progress

**Completed:**
- Data collection and analysis (60 destinations)
- Feature engineering pipeline
- Cost categorization system (budget/mid/premium/luxury)
- Quality scoring algorithms (popularity + safety weighted)
- User preference matching system
- **ML recommendation engine with explainable scoring**
- **Multi-stage filtering and ranking algorithm**
- **Comprehensive testing with different user profiles**

**Next:**
- Performance evaluation and optimization
- Web interface development

## Getting Started

```bash
pip install -r requirements.txt
python demo.py
```

The demo script shows the recommendation system in action with different user profiles.