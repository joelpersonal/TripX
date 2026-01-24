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
│   ├── 04_recommendation_testing.ipynb # Algorithm testing
│   └── 05_evaluation_improvements.ipynb # Evaluation & improvements
├── src/
│   ├── prep.py                         # Data preprocessing
│   ├── recsys.py                       # Recommendation engine
│   ├── evaluation.py                   # Evaluation framework
│   ├── improvements.py                 # Algorithm enhancements
│   └── ab_testing.py                   # A/B testing framework
├── demo.py                             # Quick demo script
├── app.py                              # Streamlit interface
└── requirements.txt
```

## Dataset

The system uses a comprehensive global dataset of 320+ travel destinations with features like:
- **Global Coverage**: 190+ countries across all 6 continents
- **Price Range**: $12-300 per day covering budget to luxury travel
- **Trip Duration**: 1-28 days optimal stay recommendations
- **Travel Styles**: Culture, beach, urban, luxury, nature experiences
- **Seasonal Data**: Best travel seasons and climate information
- **Quality Metrics**: Popularity and safety scores for each destination

## Technical Approach

**Data Processing**: Cost categorization, duration compatibility scoring, quality indicators
**ML Strategy**: Multi-stage filtering and similarity-based ranking
**Features**: Engineered features for budget matching, preference scoring, and quality ranking

## Development Progress

**Completed:**
- Data collection and analysis (320+ destinations globally)
- Feature engineering pipeline
- Cost categorization system (budget/mid/premium/luxury)
- Quality scoring algorithms (popularity + safety weighted)
- User preference matching system
- **ML recommendation engine with explainable scoring**
- **Multi-stage filtering and ranking algorithm**
- **Comprehensive testing with different user profiles**
- **Advanced evaluation framework with performance metrics**
- **Algorithm improvements with enhanced scoring and diversity**
- **A/B testing framework for algorithm comparison**
- **Statistical validation and performance benchmarking**
- **Global dataset expansion (190+ countries, all continents)**
- **✅ LLM & API Integration (Day 6 Complete)**
  - Free LLM integration (Groq API with LLaMA-3)
  - Weather API integration (Open-Meteo)
  - Attractions API integration (OpenTripMap)
  - Enhanced recommendations with natural language explanations
  - Complete ML + LLM + API pipeline operational

**Next:**
- Day 7: Streamlit UI development and deployment preparation

## Getting Started

```bash
pip install -r requirements.txt
python demo.py
```

The demo script shows the recommendation system in action with different user profiles.