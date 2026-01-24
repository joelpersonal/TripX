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
        with st.spinner("🔧 Loading TripX AI Engine..."):
            st.session_state.engine = TripXIntegratedEngine("groq")
    return st.session_state.engine


def create_score_chart(recommendations):
    """Create a bar chart showing ML scores"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    scores = [rec['ml_score'] for rec in recommendations]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=scores,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'][:len(destinations)],
            text=[f"{score:.3f}" for score in scores],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="🎯 ML Recommendation Scores",
        xaxis_title="Destinations",
        yaxis_title="ML Score",
        yaxis=dict(range=[0, 1]),
        height=400,
        showlegend=False
    )
    
    return fig


def create_cost_comparison(recommendations):
    """Create cost comparison chart"""
    if not recommendations:
        return None
    
    destinations = [rec['ml_recommendation']['destination'] for rec in recommendations]
    costs = [rec['ml_recommendation']['cost_per_day'] for rec in recommendations]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=costs,
            marker_color='#74B9FF',
            text=[f"${cost}/day" for cost in costs],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="💰 Daily Cost Comparison",
        xaxis_title="Destinations",
        yaxis_title="Cost per Day ($)",
        height=400,
        showlegend=False
    )
    
    return fig


def display_recommendation_card(rec, rank):
    """Display a single recommendation as a card"""
    ml_rec = rec['ml_recommendation']
    
    with st.container():
        st.markdown(f"""
        <div style="
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        ">
            <h3>🏆 #{rank} - {ml_rec['destination']}, {ml_rec['country']}</h3>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span><strong>🎯 ML Score:</strong> {rec['ml_score']:.3f}</span>
                <span><strong>💰 Cost:</strong> ${ml_rec['cost_per_day']}/day</span>
                <span><strong>⏱️ Duration:</strong> {ml_rec['duration_range']}</span>
            </div>
            <div style="margin: 10px 0;">
                <strong>🎨 Trip Type:</strong> {ml_rec['trip_type']} | 
                <strong>🌍 Region:</strong> {ml_rec['region']} | 
                <strong>🌤️ Weather:</strong> {rec['weather_info'].get('current_temp', 'N/A')}°C
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🧠 ML Analysis:**")
            st.write(rec['ml_reasoning'])
            
            st.markdown("**🏛️ Top Attractions:**")
            for i, attraction in enumerate(rec['attractions'][:3], 1):
                st.write(f"{i}. {attraction['name']} ({attraction['category']})")
        
        with col2:
            st.markdown("**🤖 AI Explanation:**")
            st.write(rec['llm_explanation'])
            
            st.markdown("**📝 Sample Itinerary:**")
            itinerary_preview = rec['detailed_itinerary'][:300] + "..." if len(rec['detailed_itinerary']) > 300 else rec['detailed_itinerary']
            st.write(itinerary_preview)


def main():
    st.set_page_config(
        page_title="TripX - AI Travel Recommendations",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 30px;">
        <h1>🌍 TripX - AI Travel Recommendations</h1>
        <p>ML-Driven Personalized Travel Planning with LLM Enhancement</p>
        <p><em>Architecture: ML (Decisions) + LLM (Text) + APIs (Enrichment)</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("🎯 Your Travel Preferences")
        
        # Budget input
        budget = st.slider(
            "💰 Daily Budget ($)",
            min_value=20,
            max_value=500,
            value=100,
            step=10,
            help="Your maximum budget per day"
        )
        
        # Duration input
        duration = st.slider(
            "⏱️ Trip Duration (days)",
            min_value=1,
            max_value=30,
            value=7,
            step=1,
            help="How many days you want to travel"
        )
        
        # Trip type selection
        trip_type = st.selectbox(
            "🎨 Trip Type",
            options=["culture", "beach", "urban", "luxury", "nature"],
            index=0,
            help="What type of travel experience you prefer"
        )
        
        # Season selection
        season = st.selectbox(
            "🌤️ Travel Season",
            options=["spring", "summer", "autumn", "winter"],
            index=0,
            help="When you plan to travel"
        )
        
        # Number of recommendations
        num_recommendations = st.slider(
            "📊 Number of Recommendations",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="How many destinations to recommend"
        )
        
        st.markdown("---")
        
        # Get recommendations button
        if st.button("🚀 Get AI Recommendations", type="primary"):
            user_preferences = {
                "budget": budget,
                "duration": duration,
                "trip_type": trip_type,
                "season": season
            }
            
            st.session_state.user_preferences = user_preferences
            
            # Load engine and get recommendations
            engine = load_engine()
            
            with st.spinner("🧠 AI is analyzing destinations..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                results = engine.get_enhanced_recommendations(
                    user_preferences, 
                    top_n=num_recommendations
                )
                
                st.session_state.recommendations = results
            
            st.success("✅ Recommendations ready!")
    
    # Main content area
    if st.session_state.recommendations is None:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 40px; border: 2px dashed #ccc; border-radius: 10px;">
                <h2>🎯 Welcome to TripX!</h2>
                <p>Set your preferences in the sidebar and click <strong>"Get AI Recommendations"</strong> to discover your perfect travel destinations.</p>
                <br>
                <h3>🏗️ How It Works:</h3>
                <p><strong>1. ML Engine:</strong> Analyzes 320+ destinations with 27 features</p>
                <p><strong>2. LLM Enhancement:</strong> Generates natural language explanations</p>
                <p><strong>3. API Enrichment:</strong> Adds weather and attraction data</p>
            </div>
            """, unsafe_allow_html=True)
            
            # System stats
            engine = load_engine()
            if engine:
                st.markdown("### 📊 System Statistics")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("🌍 Destinations", "320+")
                
                with col_b:
                    st.metric("🧠 ML Features", "27")
                
                with col_c:
                    st.metric("🏛️ Countries", "190+")
    
    else:
        results = st.session_state.recommendations
        
        if results['status'] == 'success':
            # Display user preferences
            prefs = st.session_state.user_preferences
            st.markdown(f"""
            **👤 Your Profile:** Budget ${prefs['budget']}/day | {prefs['duration']} days | {prefs['trip_type']} travel | {prefs['season']} season
            """)
            
            # Success message
            st.success(f"✅ Found {results['total_recommendations']} perfect matches from {results['ml_engine_info']['total_destinations']} destinations!")
            
            # Charts
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
            st.markdown("## 🏆 Your Personalized Recommendations")
            
            for i, rec in enumerate(results['recommendations'], 1):
                display_recommendation_card(rec, i)
            
            # Comparison report
            if len(results['recommendations']) >= 2:
                st.markdown("## 🔍 AI Comparison Analysis")
                
                with st.spinner("🤖 Generating comparison report..."):
                    comparison = st.session_state.engine.generate_comparison_report(
                        st.session_state.user_preferences
                    )
                
                if comparison['status'] == 'success':
                    st.markdown(f"""
                    <div style="
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 5px solid #007bff;
                    ">
                        <h4>🤖 AI Analysis:</h4>
                        <p>{comparison['comparison_analysis']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # System info
            st.markdown("---")
            st.markdown("### 🔧 System Information")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🧠 ML Algorithm", "Multi-Factor Weighted")
            
            with col2:
                st.metric("🤖 LLM Provider", "Groq (LLaMA-3)")
            
            with col3:
                st.metric("🌤️ Weather API", "Open-Meteo")
            
            with col4:
                st.metric("🏛️ Attractions API", "OpenTripMap")
        
        else:
            st.error(f"❌ No recommendations found: {results.get('message', 'Unknown error')}")
            st.info("💡 Try adjusting your preferences (budget, duration, or trip type) for more options.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌍 <strong>TripX</strong> - ML-Driven Travel Recommendations | 
        Built with ❤️ using Streamlit, Python ML, and Free APIs</p>
        <p><em>Architecture: ML (Core Intelligence) + LLM (Text Generation) + APIs (Data Enrichment)</em></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()