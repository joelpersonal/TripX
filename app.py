import streamlit as st
import sys
import os
sys.path.append('src')

from integrated_engine import TripXIntegratedEngine
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time


def apply_black_white_theme():
    """
    Apply ultra-professional black & white theme to Streamlit UI
    
    Design Philosophy:
    - Corporate-grade minimalism with sophisticated typography
    - Maximum contrast for accessibility and readability
    - Clean geometric layouts with precise spacing
    - Professional color palette suitable for executive presentations
    """
    st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-tertiary: #1a1a1a;
        --text-primary: #FFFFFF;
        --text-secondary: #E5E5E5;
        --text-muted: #999999;
        --border-color: #2a2a2a;
        --accent-color: #FFFFFF;
        --shadow: 0 2px 8px rgba(255,255,255,0.05);
    }
    
    /* Main app styling */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar professional styling */
    .css-1d391kg, .css-1cypcdb {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    /* Main content container */
    .main .block-container {
        background-color: var(--bg-primary);
        padding: 3rem 2rem;
        max-width: 1200px;
    }
    
    /* Professional typography hierarchy */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.2 !important;
    }
    
    h1 { font-size: 2.5rem !important; font-weight: 300 !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4 { font-size: 1.25rem !important; }
    
    /* Body text styling */
    p, div, span, label {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Professional header section */
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 3rem;
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
    /* Executive-style cards */
    .executive-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .executive-card:hover {
        border-color: var(--accent-color);
        box-shadow: 0 4px 16px rgba(255,255,255,0.1);
        transform: translateY(-2px);
    }
    
    /* Professional metrics display */
    .metric-card {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: var(--bg-secondary);
        border-color: var(--accent-color);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Enhanced input styling */
    .stSelectbox > div > div, .stSlider > div {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1a1a 100%) !important;
        color: var(--text-primary) !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.025em !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        font-size: 0.875rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border-color: var(--text-primary) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(255,255,255,0.1) !important;
    }
    
    /* Professional section dividers */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border-color) 50%, transparent 100%);
        margin: 3rem 0;
    }
    
    /* Status indicators */
    .status-success {
        background: var(--bg-tertiary);
        border-left: 4px solid var(--accent-color);
        padding: 1rem 1.5rem;
        border-radius: 0 6px 6px 0;
        margin: 1rem 0;
    }
    
    .status-info {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        padding: 1rem 1.5rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Enhanced progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, #e0e0e0 100%) !important;
        border-radius: 4px !important;
    }
    
    /* Professional sidebar styling */
    .sidebar-section {
        background: var(--bg-tertiary);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Footer styling */
    .professional-footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
        background: var(--bg-secondary);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 2rem 1rem;
        }
        
        .executive-card {
            padding: 1.5rem;
        }
        
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables - Backend logic unchanged"""
    if 'engine' not in st.session_state:
        st.session_state.engine = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = None


def load_engine():
    """Load the TripX integrated engine - Backend logic unchanged"""
    if st.session_state.engine is None:
        with st.spinner("Loading TripX AI Engine..."):
            st.session_state.engine = TripXIntegratedEngine("groq")
    return st.session_state.engine


def create_score_chart(recommendations):
    """Create professional black & white themed bar chart showing ML scores"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    scores = [rec['ml_score'] for rec in recommendations]
    
    # Professional grayscale gradient
    colors = ['#FFFFFF', '#E0E0E0', '#C0C0C0', '#A0A0A0', '#808080'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='#000000', width=1.5),
                pattern_shape="",
            ),
            text=[f"{score:.3f}" for score in scores],
            textposition='auto',
            textfont=dict(
                color='#000000', 
                size=14, 
                family='Inter, sans-serif'
            ),
            hovertemplate='<b>%{x}</b><br>ML Score: %{y:.3f}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="ML Recommendation Scores",
            font=dict(color='#FFFFFF', size=20, family='Inter, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Destinations",
            title_font=dict(color='#FFFFFF', size=14, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2a2a2a',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="ML Score",
            range=[0, 1],
            title_font=dict(color='#FFFFFF', size=14, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2a2a2a',
            showgrid=True,
            zeroline=False
        ),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        height=450,
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(family='Inter, sans-serif')
    )
    
    return fig


def create_cost_comparison(recommendations):
    """Create professional black & white themed cost comparison chart"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    costs = [rec['ml_recommendation']['cost_per_day'] for rec in recommendations]
    
    # Professional grayscale gradient for costs
    colors = ['#FFFFFF', '#E0E0E0', '#C0C0C0', '#A0A0A0', '#808080'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=costs,
            marker=dict(
                color=colors,
                line=dict(color='#000000', width=1.5),
                pattern_shape="",
            ),
            text=[f"${cost}" for cost in costs],
            textposition='auto',
            textfont=dict(
                color='#000000', 
                size=14, 
                family='Inter, sans-serif'
            ),
            hovertemplate='<b>%{x}</b><br>Cost: $%{y}/day<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Daily Cost Comparison",
            font=dict(color='#FFFFFF', size=20, family='Inter, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Destinations",
            title_font=dict(color='#FFFFFF', size=14, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2a2a2a',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Cost per Day ($)",
            title_font=dict(color='#FFFFFF', size=14, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2a2a2a',
            showgrid=True,
            zeroline=False
        ),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        height=450,
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(family='Inter, sans-serif')
    )
    
    return fig


def display_recommendation_card(rec, rank):
    """Display a single recommendation as a minimalist black & white card"""
    ml_rec = rec['ml_recommendation']
    
    # Create a clean card using Streamlit components
    with st.container():
        # Header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); 
                    border: 1px solid #2a2a2a; border-radius: 12px; padding: 2rem; 
                    margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(255,255,255,0.05);">
            <h3 style="color: #FFFFFF; margin-bottom: 1.5rem; font-weight: 300; font-size: 1.5rem;">
                #{rank} — {ml_rec['destination']}, {ml_rec['country']}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #1a1a1a; border-radius: 8px; margin: 0.5rem 0;">
                <div style="color: #CCCCCC; font-size: 0.8rem; margin-bottom: 0.5rem;">ML SCORE</div>
                <div style="color: #FFFFFF; font-size: 1.4rem; font-weight: 500;">{rec['ml_score']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #1a1a1a; border-radius: 8px; margin: 0.5rem 0;">
                <div style="color: #CCCCCC; font-size: 0.8rem; margin-bottom: 0.5rem;">COST</div>
                <div style="color: #FFFFFF; font-size: 1.4rem; font-weight: 500;">${ml_rec['cost_per_day']}/day</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #1a1a1a; border-radius: 8px; margin: 0.5rem 0;">
                <div style="color: #CCCCCC; font-size: 0.8rem; margin-bottom: 0.5rem;">DURATION</div>
                <div style="color: #FFFFFF; font-size: 1.4rem; font-weight: 500;">{ml_rec['duration_range']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Details row
        st.markdown(f"""
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                    border-top: 1px solid #333333;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <span style="color: #CCCCCC;"><strong style="color: #FFFFFF;">Type:</strong> {ml_rec['trip_type']}</span>
                <span style="color: #CCCCCC;"><strong style="color: #FFFFFF;">Region:</strong> {ml_rec['region']}</span>
                <span style="color: #CCCCCC;"><strong style="color: #FFFFFF;">Weather:</strong> {rec['weather_info'].get('current_temp', 'N/A')}°C</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content sections with clean layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ML ANALYSIS**")
            st.write(rec['ml_reasoning'])
            
            st.markdown("**TOP ATTRACTIONS**")
            for i, attraction in enumerate(rec['attractions'][:3], 1):
                st.write(f"{i}. {attraction['name']} ({attraction['category']})")
        
        with col2:
            st.markdown("**AI EXPLANATION**")
            st.write(rec['llm_explanation'])
            
            st.markdown("**SAMPLE ITINERARY**")
            itinerary_preview = rec['detailed_itinerary'][:300] + "..." if len(rec['detailed_itinerary']) > 300 else rec['detailed_itinerary']
            st.write(itinerary_preview)
        
        # Add separator
        st.markdown("""
        <div style="border-top: 1px solid #333333; margin: 2rem 0;"></div>
        """, unsafe_allow_html=True)


def main():
    """
    Main Streamlit application with professional black & white theme
    
    UI Design Philosophy:
    - Streamlit is the primary UI framework for its ML-focused simplicity
    - Black & white theme provides clean, professional appearance
    - Minimalist design reduces distractions and focuses on data
    - React components (if added) are only for UI customization, not business logic
    """
    st.set_page_config(
        page_title="TripX - AI Travel Recommendations",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply professional theme and initialize
    apply_black_white_theme()
    initialize_session_state()
    
    # Ultra-professional header with executive styling
    st.markdown("""
    <div class="main-header fade-in">
        <h1 style="color: #FFFFFF; font-size: 3rem; font-weight: 300; margin: 0; letter-spacing: -0.02em;">
            TripX
        </h1>
        <p style="color: #E5E5E5; font-size: 1.1rem; margin: 0.75rem 0 0 0; font-weight: 400;">
            AI-Driven Travel Intelligence Platform
        </p>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #2a2a2a;">
            <span style="color: #999999; font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em;">
                Machine Learning • Natural Language Processing • Real-time Data
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional sidebar with executive-style controls
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-section">
            <h3 style="color: #FFFFFF; font-weight: 500; margin: 0 0 1rem 0; font-size: 1.25rem;">
                Travel Preferences
            </h3>
            <p style="color: #999999; font-size: 0.875rem; margin: 0 0 1.5rem 0; line-height: 1.4;">
                Configure your ideal travel parameters for personalized AI recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced budget input
        st.markdown("**Budget Range**")
        budget = st.slider(
            "Daily Budget ($)",
            min_value=20,
            max_value=500,
            value=100,
            step=10,
            help="Your maximum budget per day for accommodation, meals, and activities"
        )
        st.markdown(f"<p style='color: #999999; font-size: 0.8rem; margin-top: -0.5rem;'>Selected: ${budget}/day</p>", unsafe_allow_html=True)
        
        # Enhanced duration input
        st.markdown("**Trip Duration**")
        duration = st.slider(
            "Trip Duration (days)",
            min_value=1,
            max_value=30,
            value=7,
            step=1,
            help="Total number of days for your travel experience"
        )
        st.markdown(f"<p style='color: #999999; font-size: 0.8rem; margin-top: -0.5rem;'>Selected: {duration} days</p>", unsafe_allow_html=True)
        
        # Enhanced trip type selection
        st.markdown("**Travel Style**")
        trip_type = st.selectbox(
            "Trip Type",
            options=["culture", "beach", "urban", "luxury", "nature"],
            index=0,
            help="Primary focus and style of your travel experience"
        )
        
        # Enhanced season selection
        st.markdown("**Travel Season**")
        season = st.selectbox(
            "Season",
            options=["spring", "summer", "autumn", "winter"],
            index=0,
            help="Preferred season for optimal weather and activities"
        )
        
        # Enhanced recommendations count
        st.markdown("**Results Count**")
        num_recommendations = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="How many destination recommendations to generate"
        )
        
        st.markdown("<div style='border-top: 1px solid #333333; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Get recommendations button
        if st.button("Get AI Recommendations", type="primary"):
            user_preferences = {
                "budget": budget,
                "duration": duration,
                "trip_type": trip_type,
                "season": season
            }
            
            st.session_state.user_preferences = user_preferences
            
            # Load engine and get recommendations - Backend logic unchanged
            engine = load_engine()
            
            with st.spinner("AI is analyzing destinations..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                results = engine.get_enhanced_recommendations(
                    user_preferences, 
                    top_n=num_recommendations
                )
                
                st.session_state.recommendations = results
            
            st.success("Recommendations ready!")
    
    # Main content area with clean layout
    if st.session_state.recommendations is None:
        # Welcome screen with minimalist design
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <h2 style="color: #FFFFFF; font-weight: 300; margin-bottom: 1rem; font-size: 2rem;">
                    Welcome to TripX
                </h2>
                <p style="color: #CCCCCC; line-height: 1.6; margin-bottom: 2rem; font-size: 1.1rem;">
                    Set your preferences in the sidebar and click <strong>"Get AI Recommendations"</strong> 
                    to discover your perfect travel destinations.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add separator
            st.markdown("""
            <div style="border-top: 1px solid #333333; margin: 1.5rem 0;"></div>
            """, unsafe_allow_html=True)
            
            # How it works section using Streamlit components
            st.markdown("""
            <h3 style="color: #FFFFFF; font-weight: 300; margin-bottom: 1rem; text-align: center;">
                How It Works
            </h3>
            """, unsafe_allow_html=True)
            
            # Use Streamlit text instead of HTML
            st.write("**1. ML Engine:** Analyzes 320+ destinations with 27 features")
            st.write("**2. LLM Enhancement:** Generates natural language explanations")
            st.write("**3. API Enrichment:** Adds weather and attraction data")
            
            # System stats with clean metrics
            engine = load_engine()
            if engine:
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                st.markdown("### System Statistics")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="text-align: center;">
                            <div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 500;">320+</div>
                            <div style="color: #CCCCCC; font-size: 0.8rem;">DESTINATIONS</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="text-align: center;">
                            <div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 500;">27</div>
                            <div style="color: #CCCCCC; font-size: 0.8rem;">ML FEATURES</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_c:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="text-align: center;">
                            <div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 500;">190+</div>
                            <div style="color: #CCCCCC; font-size: 0.8rem;">COUNTRIES</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        results = st.session_state.recommendations
        
        if results['status'] == 'success':
            # Display user preferences with clean styling
            prefs = st.session_state.user_preferences
            st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border-left: 3px solid #FFFFFF;">
                <strong style="color: #FFFFFF;">Your Profile:</strong> 
                <span style="color: #CCCCCC;">
                    Budget ${prefs['budget']}/day • {prefs['duration']} days • {prefs['trip_type']} travel • {prefs['season']} season
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Success message with clean styling
            st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border-left: 3px solid #FFFFFF;">
                <span style="color: #FFFFFF;">
                    Found {results['total_recommendations']} perfect matches from {results['ml_engine_info']['total_destinations']} destinations
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Charts section with clean layout
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            st.markdown("### Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                score_chart = create_score_chart(results['recommendations'])
                if score_chart:
                    st.plotly_chart(score_chart, width='stretch')
            
            with col2:
                cost_chart = create_cost_comparison(results['recommendations'])
                if cost_chart:
                    st.plotly_chart(cost_chart, width='stretch')
            
            # Display recommendations with clean cards
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            st.markdown("### Your Personalized Recommendations")
            
            for i, rec in enumerate(results['recommendations'], 1):
                display_recommendation_card(rec, i)
            
            # Comparison report with minimalist design
            if len(results['recommendations']) >= 2:
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                st.markdown("### AI Comparison Analysis")
                
                with st.spinner("Generating comparison report..."):
                    comparison = st.session_state.engine.generate_comparison_report(
                        st.session_state.user_preferences
                    )
                
                if comparison['status'] == 'success':
                    st.markdown(f"""
                    <div style="
                        background-color: #1a1a1a;
                        padding: 1.5rem;
                        border-radius: 8px;
                        border-left: 3px solid #FFFFFF;
                        margin: 1rem 0;
                    ">
                        <h4 style="color: #FFFFFF; margin-bottom: 1rem; font-weight: 300;">AI Analysis</h4>
                        <p style="color: #CCCCCC; line-height: 1.6; margin: 0;">{comparison['comparison_analysis']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # System info with clean metrics
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            st.markdown("### System Information")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-container">
                    <div style="text-align: center;">
                        <div style="color: #FFFFFF; font-size: 1rem; font-weight: 500;">Multi-Factor Weighted</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem;">ML ALGORITHM</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-container">
                    <div style="text-align: center;">
                        <div style="color: #FFFFFF; font-size: 1rem; font-weight: 500;">Groq (LLaMA-3)</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem;">LLM PROVIDER</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-container">
                    <div style="text-align: center;">
                        <div style="color: #FFFFFF; font-size: 1rem; font-weight: 500;">Open-Meteo</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem;">WEATHER API</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric-container">
                    <div style="text-align: center;">
                        <div style="color: #FFFFFF; font-size: 1rem; font-weight: 500;">OpenTripMap</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem;">ATTRACTIONS API</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border-left: 3px solid #666666; margin: 1rem 0;">
                <h4 style="color: #FFFFFF; margin-bottom: 0.5rem;">No Recommendations Found</h4>
                <p style="color: #CCCCCC; margin: 0.5rem 0;">{results.get('message', 'Unknown error')}</p>
                <p style="color: #888888; font-size: 0.9rem; margin: 0;">
                    Try adjusting your preferences (budget, duration, or trip type) for more options.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with minimalist design
    st.markdown("""
    <div class="footer">
        <p style="margin: 0;">
            <strong>TripX</strong> — ML-Driven Travel Recommendations
        </p>
        <p style="margin: 0.25rem 0 0 0; font-size: 0.7rem;">
            Built with Streamlit • Python ML • Free APIs
        </p>
        <p style="margin: 0.25rem 0 0 0; font-size: 0.7rem;">
            Architecture: ML (Core Intelligence) + LLM (Text Generation) + APIs (Data Enrichment)
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()