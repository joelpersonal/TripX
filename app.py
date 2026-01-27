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
import base64





def apply_simple_theme():
    """Apply minimal styling for simple UI"""
    st.markdown("""
    <style>
    /* Simple dark theme */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Simple text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Simple input styling */
    .stNumberInput > div > div > input {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #666666 !important;
    }
    
    .stSelectbox > div > div {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #666666 !important;
    }
    
    /* Simple button styling */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background-color: #CCCCCC !important;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'engine' not in st.session_state:
        st.session_state.engine = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = None


def load_engine():
    """Load the TripX integrated engine"""
    if st.session_state.engine is None:
        with st.spinner("Loading TripX AI Engine..."):
            st.session_state.engine = TripXIntegratedEngine("groq")
    return st.session_state.engine


def create_score_chart(recommendations):
    """Create bar chart showing ML scores"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    scores = [rec['ml_score'] for rec in recommendations]
    
    # Black and white gradient colors
    colors = ['#FFFFFF', '#CCCCCC', '#999999', '#666666', '#333333'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=2),
                pattern_shape="",
            ),
            text=[f"{score:.3f}" for score in scores],
            textposition='auto',
            textfont=dict(
                color='#000000', 
                size=14, 
                family='Inter, sans-serif',
                weight='bold'
            ),
            hovertemplate='<b>%{x}</b><br>ML Score: %{y:.3f}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Machine Learning Recommendation Scores",
            font=dict(color='#FFFFFF', size=22, family='Inter, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Destinations",
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#CCCCCC', size=12, family='Inter, sans-serif'),
            gridcolor='#666666',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="ML Confidence Score",
            range=[0, 1],
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#CCCCCC', size=12, family='Inter, sans-serif'),
            gridcolor='#666666',
            showgrid=True,
            zeroline=False
        ),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        height=450,
        showlegend=False,
        margin=dict(l=70, r=70, t=90, b=70),
        font=dict(family='Inter, sans-serif')
    )
    
    return fig


def create_cost_comparison(recommendations):
    """Create cost comparison chart"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    costs = [rec['ml_recommendation']['cost_per_day'] for rec in recommendations]
    
    # Black and white gradient colors for costs
    colors = ['#FFFFFF', '#CCCCCC', '#999999', '#666666', '#333333'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=costs,
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=2),
                pattern_shape="",
            ),
            text=[f"${cost}" for cost in costs],
            textposition='auto',
            textfont=dict(
                color='#000000', 
                size=14, 
                family='Inter, sans-serif',
                weight='bold'
            ),
            hovertemplate='<b>%{x}</b><br>Cost: $%{y}/day<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Daily Cost Analysis",
            font=dict(color='#FFFFFF', size=22, family='Inter, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Destinations",
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#CCCCCC', size=12, family='Inter, sans-serif'),
            gridcolor='#666666',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Cost per Day (USD)",
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#CCCCCC', size=12, family='Inter, sans-serif'),
            gridcolor='#666666',
            showgrid=True,
            zeroline=False
        ),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        height=450,
        showlegend=False,
        margin=dict(l=70, r=70, t=90, b=70),
        font=dict(family='Inter, sans-serif')
    )
    
    return fig



def main():
    """Simple Streamlit application with native components"""
    st.set_page_config(
        page_title="TripX - AI Travel Recommendations",
        page_icon="images/tripX_logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply simple theme and initialize
    apply_simple_theme()
    initialize_session_state()
    
    # Simple header
    st.title("Hey there, traveler!")
    st.subheader("Welcome to TripX")
    
    st.write("""
    I'm here to help you discover your next amazing adventure! Tell me what you're looking for, 
    and I'll use some pretty smart AI to find destinations that match your vibe perfectly.
    """)
    
    st.write("""
    Think of me as your personal travel buddy who happens to know about **320+ destinations** 
    across **190+ countries**. I'll consider everything from your budget to the weather, 
    local attractions, and even safety ratings to suggest places you'll absolutely love.
    """)
    
    st.info("Ready to find your perfect getaway?")
    
    # Main configuration section
    if st.session_state.recommendations is None:
        st.header("Let's plan your perfect trip!")
        st.write("""
        Just fill out a few details below, and I'll work my magic to find destinations that are 
        absolutely perfect for you. Don't worry - this only takes a minute!
        """)
        
        # Simple form using native Streamlit components
        with st.form("recommendation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("What's your daily budget?")
                st.write("This includes accommodation, meals, and activities. Don't worry, I'll find great options within your range!")
                budget = st.number_input(
                    "Daily Budget (USD)",
                    min_value=1,
                    max_value=10000,
                    value=100,
                    step=1,
                    help="How much are you comfortable spending per day?"
                )
                st.write(f"Perfect! I'll look for places around **${budget} per day**")
            
            with col2:
                st.subheader("How long is your trip?")
                st.write("Whether it's a quick weekend getaway or a month-long adventure, I'll match you with the right destinations.")
                duration = st.number_input(
                    "Trip Duration (days)",
                    min_value=1,
                    max_value=365,
                    value=7,
                    step=1,
                    help="How many days will you be traveling?"
                )
                st.write(f"Got it! **{duration} days** sounds like a great trip length")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("What kind of vibe are you going for?")
                st.write("Are you more of a museum-hopper, beach-lounger, city explorer, luxury traveler, or nature lover?")
                
                trip_type_options = {
                    "culture": "Culture & History (museums, temples, local traditions)",
                    "beach": "Beach & Relaxation (sun, sand, and chill vibes)",
                    "urban": "City Life (nightlife, shopping, urban experiences)",
                    "luxury": "Luxury Travel (high-end experiences and comfort)",
                    "nature": "Nature & Adventure (hiking, wildlife, outdoor activities)"
                }
                
                trip_type = st.selectbox(
                    "What's your travel style?",
                    options=list(trip_type_options.keys()),
                    format_func=lambda x: trip_type_options[x],
                    index=0,
                    help="Pick the style that sounds most exciting to you!"
                )
            
            with col4:
                st.subheader("When are you thinking of going?")
                st.write("Different seasons mean different experiences - cherry blossoms in spring, summer festivals, autumn colors, or cozy winter vibes.")
                
                season_options = {
                    "spring": "Spring (March-May) - Perfect weather, blooming flowers",
                    "summer": "Summer (June-August) - Warm weather, festivals, long days",
                    "autumn": "Autumn (September-November) - Beautiful colors, mild weather",
                    "winter": "Winter (December-February) - Cozy vibes, winter activities"
                }
                
                season = st.selectbox(
                    "Which season speaks to you?",
                    options=list(season_options.keys()),
                    format_func=lambda x: season_options[x],
                    index=0,
                    help="Each season has its own magic - what sounds good to you?"
                )
            
            st.subheader("How many options would you like?")
            st.write("I can give you anywhere from 1 to 10 personalized recommendations. More options = more choices!")
            num_recommendations = st.number_input(
                "Number of destination suggestions",
                min_value=1,
                max_value=10,
                value=3,
                step=1,
                help="How many different destinations would you like me to suggest?"
            )
            st.write(f"Great! I'll find you **{num_recommendations} amazing destinations**")
            
            st.subheader("Alright, let's do this!")
            st.write("""
            I'm excited to show you some incredible places that match exactly what you're looking for. 
            This might take a moment while I analyze all the possibilities...
            """)
            
            submitted = st.form_submit_button(
                "Find My Perfect Destinations!",
                help="Click here and let me work my magic!"
            )
            
            if submitted:
                user_preferences = {
                    "budget": budget,
                    "duration": duration,
                    "trip_type": trip_type,
                    "season": season
                }
                
                st.session_state.user_preferences = user_preferences
                
                # Load engine and get recommendations
                engine = load_engine()
                
                with st.spinner("Hold on, I'm thinking really hard about this..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    results = engine.get_enhanced_recommendations(
                        user_preferences, 
                        top_n=num_recommendations
                    )
                    
                    st.session_state.recommendations = results
                
                st.success("Ta-da! I found some amazing places for you!")
                st.rerun()
        
        # Simple system info
        st.divider()
        st.header("Powered by Advanced AI Technology")
        st.write("Our intelligent system combines multiple AI technologies to deliver precise, personalized travel recommendations")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Core Engine", "ML", help="Advanced algorithms analyzing 320+ destinations with 27 engineered features")
        
        with col_b:
            st.metric("Language Processing", "NLP", help="Natural language generation for comprehensive travel explanations")
        
        with col_c:
            st.metric("Data Integration", "API", help="Real-time weather and attraction data enrichment")
        
        # System statistics
        engine = load_engine()
        if engine:
            st.divider()
            st.subheader("System Performance Metrics")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Global Destinations", "320+")
            
            with col_b:
                st.metric("ML Features", "27")
            
            with col_c:
                st.metric("Countries", "190+")

    else:
        results = st.session_state.recommendations
        
        # Back button
        if st.button("← Back to Configuration"):
            st.session_state.recommendations = None
            st.session_state.user_preferences = None
            st.rerun()
        
        if results['status'] == 'success':
            # Display user preferences
            prefs = st.session_state.user_preferences
            st.info(f"**Your Profile:** Budget ${prefs['budget']}/day • {prefs['duration']} days • {prefs['trip_type']} travel • {prefs['season']} season")
            
            # Success message
            st.success(f"Found {results['total_recommendations']} perfect matches from {results['ml_engine_info']['total_destinations']} destinations")
            
            # Charts section
            st.divider()
            st.subheader("Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                score_chart = create_score_chart(results['recommendations'])
                if score_chart:
                    st.plotly_chart(score_chart, use_container_width=True)
            
            with col2:
                cost_chart = create_cost_comparison(results['recommendations'])
                if cost_chart:
                    st.plotly_chart(cost_chart, use_container_width=True)
            
            # Display recommendations
            st.divider()
            st.subheader("Your Personalized Recommendations")
            
            for i, rec in enumerate(results['recommendations'], 1):
                ml_rec = rec['ml_recommendation']
                
                with st.expander(f"#{i} - {ml_rec['destination']}, {ml_rec['country']} (Score: {rec['ml_score']:.3f})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("ML Score", f"{rec['ml_score']:.3f}")
                    
                    with col2:
                        st.metric("Daily Cost", f"${ml_rec['cost_per_day']}")
                    
                    with col3:
                        st.metric("Duration", ml_rec['duration_range'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Travel Type:**", ml_rec['trip_type'].title())
                        st.write("**Region:**", ml_rec['region'])
                        st.write("**Current Weather:**", f"{rec['weather_info'].get('current_temp', 'N/A')}°C")
                        
                        st.write("**Machine Learning Analysis:**")
                        st.write(rec['ml_reasoning'])
                        
                        st.write("**Key Attractions:**")
                        for j, attraction in enumerate(rec['attractions'][:3], 1):
                            st.write(f"{j}. **{attraction['name']}** ({attraction['category']})")
                    
                    with col2:
                        st.write("**AI-Generated Insights:**")
                        st.write(rec['llm_explanation'])
                        
                        st.write("**Travel Itinerary Preview:**")
                        itinerary_preview = rec['detailed_itinerary'][:300] + "..." if len(rec['detailed_itinerary']) > 300 else rec['detailed_itinerary']
                        st.write(itinerary_preview)
            
            # Comparison report
            if len(results['recommendations']) >= 2:
                st.divider()
                st.subheader("AI Comparison Analysis")
                
                with st.spinner("Generating comparison report..."):
                    comparison = st.session_state.engine.generate_comparison_report(
                        st.session_state.user_preferences
                    )
                
                if comparison['status'] == 'success':
                    st.info(comparison['comparison_analysis'])
            
            # System info
            st.divider()
            st.subheader("System Information")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("ML Algorithm", "Multi-Factor Weighted")
            
            with col2:
                st.metric("LLM Provider", "Groq (LLaMA-3)")
            
            with col3:
                st.metric("Weather API", "Open-Meteo")
            
            with col4:
                st.metric("Attractions API", "OpenTripMap")
        
        else:
            st.error("No Recommendations Found")
            st.write(results.get('message', 'Unknown error'))
            st.write("Try adjusting your preferences (budget, duration, or trip type) for more options.")
    
    # Simple footer
    st.divider()
    st.write("**TripX** — ML-Driven Travel Recommendations")
    st.caption("Built with Streamlit • Python ML • Free APIs")
    st.caption("Architecture: ML (Core Intelligence) + LLM (Text Generation) + APIs (Data Enrichment)")


if __name__ == "__main__":
    main()