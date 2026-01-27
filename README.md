# TripX - AI-Powered Travel Recommendation System

A sophisticated machine learning-driven travel recommendation platform that combines advanced algorithms, natural language processing, and real-time data integration to deliver personalized travel suggestions.

##  Project Overview

TripX is an end-to-end travel recommendation system that leverages multiple AI technologies to provide intelligent, personalized travel suggestions. The system processes user preferences through a multi-stage ML pipeline and enhances recommendations with LLM-generated insights and real-time API data.

##  Architecture & Technical Implementation

### Core ML Engine
- **Multi-Factor Scoring Algorithm**: Custom weighted scoring system combining budget compatibility, duration matching, trip type preferences, seasonal optimization, and quality metrics
- **Feature Engineering Pipeline**: 27 engineered features from 12 base attributes including cost categorization, duration compatibility scoring, and quality indicators
- **Advanced Preprocessing**: Comprehensive data transformation with categorical encoding, numerical scaling, and feature interaction terms

### AI Integration Layer
- **LLM Integration**: Natural language explanation generation using Groq API (LLaMA-3 model)
- **Weather API**: Real-time weather data integration via Open-Meteo API
- **Attractions API**: Points of interest data through OpenTripMap API
- **Hybrid Architecture**: ML for decision-making, LLM for text generation, APIs for data enrichment

### Web Application
- **Streamlit Framework**: Interactive web interface with professional black & white theme
- **Real-time Processing**: Dynamic recommendation generation with progress tracking
- **Data Visualization**: Interactive Plotly charts for ML scores and cost analysis
- **Responsive Design**: Mobile-friendly interface with custom CSS styling

## Technical Stack

**Machine Learning & Data Science**
- Python 3.8+
- Pandas & NumPy for data manipulation
- Scikit-learn for ML algorithms
- Custom recommendation engine with weighted scoring

**Web Framework & UI**
- Streamlit for web application
- Plotly for interactive visualizations
- Custom CSS for professional styling
- Responsive design principles

**AI & API Integration**
- Groq API for LLM capabilities
- Open-Meteo for weather data
- OpenTripMap for attractions
- RESTful API integration patterns

**Development & Analysis**
- Jupyter notebooks for data exploration
- Git version control
- Modular code architecture
- Comprehensive testing framework

##  Dataset & Features

**Global Coverage**: 60+ destinations across 6 continents
**Feature Set**: 27 engineered features including:
- Cost analysis (budget/mid-range/premium/luxury categories)
- Duration compatibility scoring
- Trip type matching (culture, beach, urban, luxury, nature)
- Seasonal optimization
- Safety and popularity metrics
- Climate and activity preferences

##  Key Technical Achievements

### 1. Advanced Recommendation Algorithm
```python
# Multi-factor weighted scoring system
scoring_weights = {
    'budget_fit': 0.3,
    'duration_fit': 0.2, 
    'trip_type_match': 0.25,
    'season_match': 0.15,
    'quality_bonus': 0.1
}
```

### 2. Intelligent Feature Engineering
- Cost categorization with budget compatibility scoring
- Duration range optimization algorithms
- Trip type compatibility matrix
- Seasonal preference matching
- Quality scoring (popularity + safety weighted)

### 3. Hybrid AI Architecture
- **ML Core**: Authoritative decision-making engine
- **LLM Layer**: Natural language explanation generation
- **API Enrichment**: Real-time data integration
- **Strict Separation**: Each component has defined responsibilities

### 4. Professional Web Interface
- Custom black & white corporate theme
- Interactive data visualizations
- Real-time recommendation processing
- Mobile-responsive design
- Professional typography (Inter font family)

## System Performance

**Recommendation Accuracy**: Multi-stage filtering with weighted scoring
**Processing Speed**: Real-time recommendation generation
**Scalability**: Modular architecture supporting dataset expansion
**User Experience**: Intuitive interface with comprehensive explanations

##  Getting Started

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### Installation
```bash
# Clone the repository
git clone https://github.com/joelpersonal/TripX.git
cd TripX

# Install dependencies
pip install -r requirements.txt

# Launch the application
streamlit run app.py
```

### Usage
1. **Set Preferences**: Configure budget, duration, trip type, and season
2. **Generate Recommendations**: Click "Get AI Recommendations"
3. **Analyze Results**: View ML scores, cost analysis, and detailed explanations
4. **Explore Details**: Review attractions, weather data, and sample itineraries

##  Project Structure

```
TripX/
├── data/raw/dest.csv              # Global destinations dataset
├── notebooks/                     # Data analysis & exploration
│   ├── 01_overview.ipynb         # Dataset exploration
│   ├── 02_eda.ipynb              # Exploratory data analysis
│   ├── 03_feature_engineering.ipynb # Feature development
│   └── 04_recommendation_testing.ipynb # Algorithm testing
├── src/                          # Core application modules
│   ├── prep.py                   # Data preprocessing pipeline
│   ├── recsys.py                 # ML recommendation engine
│   ├── llm_engine.py             # LLM integration layer
│   └── integrated_engine.py      # Unified system interface
├── app.py                        # Streamlit web application
├── demo.py                       # Command-line demo
└── requirements.txt              # Project dependencies
```

## Key Features

- **Intelligent Matching**: Advanced ML algorithms for personalized recommendations
- **Real-time Data**: Live weather and attraction information
- **Natural Language**: LLM-generated explanations and itineraries  
- **Interactive Visualizations**: Professional charts and analytics
- **Comprehensive Analysis**: Multi-factor scoring with detailed breakdowns
- **Scalable Architecture**: Modular design supporting future enhancements

## 🔬 Technical Highlights

**Machine Learning Engineering**
- Custom recommendation algorithm with multi-factor scoring
- Advanced feature engineering pipeline
- Comprehensive data preprocessing and validation

**Software Architecture**
- Modular, maintainable codebase
- Clear separation of concerns
- Scalable design patterns

**User Experience Design**
- Professional, corporate-grade interface
- Intuitive workflow and navigation
- Comprehensive data visualization

**API Integration**
- Multiple external service integrations
- Error handling and fallback mechanisms
- Real-time data processing

---

*Built with Python, Streamlit, and modern ML & AI practices for intelligent travel recommendations.*