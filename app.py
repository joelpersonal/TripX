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





def apply_professional_theme():
    """Apply professional black & blue theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Theme colors */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0f;
        --bg-tertiary: #1a1a2e;
        --bg-card: #16213e;
        --text-primary: #FFFFFF;
        --text-secondary: #E5E5E5;
        --text-muted: #9bb5d6;
        --border-color: #2c5aa0;
        --accent-color: #4a90e2;
        --accent-secondary: #1e3a8a;
        --accent-light: #60a5fa;
        --shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
        --shadow-hover: 0 8px 24px rgba(74, 144, 226, 0.3);
        --gradient-primary: linear-gradient(135deg, #1e3a8a 0%, #4a90e2 100%);
        --gradient-secondary: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
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
    
    /* Main content */
    .main .block-container {
        background-color: var(--bg-primary);
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem !important;
    }
    
    h1 { 
        font-size: 2.8rem !important; 
        font-weight: 300 !important; 
        text-align: center !important;
        margin-bottom: 0.5rem !important;
    }
    h2 { 
        font-size: 2.2rem !important; 
        font-weight: 400 !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding-bottom: 0.5rem !important;
    }
    h3 { 
        font-size: 1.6rem !important; 
        font-weight: 500 !important;
    }
    
    /* Header styling */
    .professional-header {
        text-align: center;
        padding: 4rem 0 3rem 0;
        border-bottom: 2px solid var(--accent-color);
        margin-bottom: 3rem;
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-tertiary) 100%);
        position: relative;
        overflow: hidden;
    }
    
    .professional-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(ellipse at center, rgba(74, 144, 226, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .professional-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--gradient-primary);
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
    }
    
    /* Cards and containers */
    .executive-card {
        background: var(--gradient-secondary);
        border: 1px solid var(--accent-color);
        border-radius: 8px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .executive-card:hover {
        border-color: var(--accent-light);
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
    
    /* Metrics */
    .metric-container {
        background: var(--bg-card);
        border: 1px solid var(--accent-color);
        border-radius: 6px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        box-shadow: var(--shadow);
    }
    
    .metric-container:hover {
        background: var(--bg-tertiary);
        border-color: var(--accent-light);
        transform: translateY(-1px);
        box-shadow: var(--shadow-hover);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--accent-light);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Button styling */
    button:not([role="slider"]):not([aria-label*="slider"]), 
    .stButton > button, 
    button[kind="primary"], 
    button[data-testid="baseButton-primary"],
    .stForm > div > div > button,
    button[kind="formSubmit"],
    .stForm button:not([role="slider"]):not([aria-label*="slider"]),
    [data-testid="stForm"] button:not([role="slider"]):not([aria-label*="slider"]),
    div[data-testid="stForm"] button:not([role="slider"]):not([aria-label*="slider"]) {
        background: var(--gradient-primary) !important;
        background-color: var(--accent-color) !important;
        color: #FFFFFF !important;
        border: 2px solid var(--accent-color) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.05em !important;
        padding: 1rem 2.5rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        box-shadow: var(--shadow) !important;
    }
    
    button:not([role="slider"]):not([aria-label*="slider"]):hover, 
    .stButton > button:hover, 
    button[kind="primary"]:hover, 
    button[data-testid="baseButton-primary"]:hover,
    .stForm > div > div > button:hover,
    button[kind="formSubmit"]:hover,
    .stForm button:not([role="slider"]):not([aria-label*="slider"]):hover,
    [data-testid="stForm"] button:not([role="slider"]):not([aria-label*="slider"]):hover,
    div[data-testid="stForm"] button:not([role="slider"]):not([aria-label*="slider"]):hover {
        background: var(--accent-light) !important;
        background-color: var(--accent-light) !important;
        color: #FFFFFF !important;
        border: 2px solid var(--accent-light) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-hover) !important;
    }
    
    /* Button text color */
    button:not([role="slider"]) span,
    .stButton > button span,
    .stForm button:not([role="slider"]) span,
    button:not([role="slider"]) p,
    .stButton > button p,
    .stForm button:not([role="slider"]) p {
        color: #FFFFFF !important;
    }
    
    /* Back button styling */
    .stButton > button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #60a5fa !important;
        border: 2px solid #4a90e2 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.05em !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2) !important;
    }
    
    .stButton > button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background: rgba(74, 144, 226, 0.1) !important;
        background-color: rgba(74, 144, 226, 0.1) !important;
        color: #FFFFFF !important;
        border: 2px solid #60a5fa !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3) !important;
    }
    
    /* Input styling */
    input, select, textarea, [role="slider"], [aria-label*="slider"], .stSlider, .stSelectbox, .stNumberInput {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--accent-color) !important;
    }
    
    .stSelectbox > div > div, .stSlider > div, .stNumberInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--accent-color) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div > input:focus {
        border-color: var(--accent-light) !important;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
    }
    
    .stNumberInput > div > div > input {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--accent-color) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        text-align: center !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-light) !important;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
        outline: none !important;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: var(--gradient-secondary);
        border: 1px solid var(--accent-color);
        border-radius: 12px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        transition: all 0.4s ease;
        position: relative;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        border-radius: 12px 12px 0 0;
    }
    
    .recommendation-card:hover {
        border-color: var(--accent-light);
        box-shadow: var(--shadow-hover);
        transform: translateY(-4px);
    }
    
    /* Section dividers */
    .section-divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent-color) 50%, transparent 100%);
        margin: 3rem 0;
    }
    
    /* Status cards */
    .status-card {
        background: var(--bg-card);
        border: 1px solid var(--accent-color);
        border-left: 4px solid var(--accent-light);
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: var(--gradient-primary) !important;
        border-radius: 4px !important;
    }
    
    /* Content sections */
    .content-section {
        background: var(--bg-card);
        border: 1px solid var(--accent-color);
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
    }
    
    /* Text styling */
    p, div, span, label {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem;
        }
        
        .recommendation-card {
            padding: 1.5rem;
        }
        
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.8rem !important; }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    </style>
    
    <script>
    // Button styling enforcement
    function forceButtonStyling() {
        const primaryButtonSelectors = [
            'button[kind="formSubmit"]',
            '.stForm > div > div > button',
            'button[data-testid="baseButton-primary"]',
            '.stButton > button'
        ];
        
        primaryButtonSelectors.forEach(selector => {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(button => {
                if (button && button.tagName === 'BUTTON' && 
                    !button.hasAttribute('role') && 
                    !button.getAttribute('aria-label')?.includes('slider') &&
                    !button.textContent.includes('Back to Configuration')) {
                    
                    // Primary button styling
                    button.style.setProperty('background', 'linear-gradient(135deg, #1e3a8a 0%, #4a90e2 100%)', 'important');
                    button.style.setProperty('background-color', '#4a90e2', 'important');
                    button.style.setProperty('color', '#FFFFFF', 'important');
                    button.style.setProperty('border', '2px solid #4a90e2', 'important');
                    button.style.setProperty('font-weight', '600', 'important');
                    button.style.setProperty('text-transform', 'uppercase', 'important');
                    button.style.setProperty('font-family', 'Inter, sans-serif', 'important');
                    button.style.setProperty('letter-spacing', '0.05em', 'important');
                    button.style.setProperty('padding', '1rem 2.5rem', 'important');
                    button.style.setProperty('font-size', '0.9rem', 'important');
                    button.style.setProperty('border-radius', '6px', 'important');
                    button.style.setProperty('cursor', 'pointer', 'important');
                    button.style.setProperty('transition', 'all 0.3s ease', 'important');
                    button.style.setProperty('box-shadow', '0 4px 12px rgba(74, 144, 226, 0.2)', 'important');
                    
                    // Text color for child elements
                    const textElements = button.querySelectorAll('*');
                    textElements.forEach(el => {
                        el.style.setProperty('color', '#FFFFFF', 'important');
                    });
                    
                    // Hover events
                    button.addEventListener('mouseenter', function() {
                        this.style.setProperty('background', '#60a5fa', 'important');
                        this.style.setProperty('background-color', '#60a5fa', 'important');
                        this.style.setProperty('border', '2px solid #60a5fa', 'important');
                        this.style.setProperty('transform', 'translateY(-2px)', 'important');
                        this.style.setProperty('box-shadow', '0 8px 24px rgba(74, 144, 226, 0.3)', 'important');
                    });
                    
                    button.addEventListener('mouseleave', function() {
                        this.style.setProperty('background', 'linear-gradient(135deg, #1e3a8a 0%, #4a90e2 100%)', 'important');
                        this.style.setProperty('background-color', '#4a90e2', 'important');
                        this.style.setProperty('border', '2px solid #4a90e2', 'important');
                        this.style.setProperty('transform', 'translateY(0px)', 'important');
                        this.style.setProperty('box-shadow', '0 4px 12px rgba(74, 144, 226, 0.2)', 'important');
                    });
                }
            });
        });
    }
    
    // Run styling
    forceButtonStyling();
    document.addEventListener('DOMContentLoaded', forceButtonStyling);
    setInterval(forceButtonStyling, 1000);
    </script>
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
    
    # Professional blue gradient colors
    colors = ['#4a90e2', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='#2c5aa0', width=2),
                pattern_shape="",
            ),
            text=[f"{score:.3f}" for score in scores],
            textposition='auto',
            textfont=dict(
                color='#FFFFFF', 
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
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2c5aa0',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="ML Confidence Score",
            range=[0, 1],
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2c5aa0',
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
    
    # Professional blue gradient colors for costs
    colors = ['#4a90e2', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8'][:len(destinations)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=destinations,
            y=costs,
            marker=dict(
                color=colors,
                line=dict(color='#2c5aa0', width=2),
                pattern_shape="",
            ),
            text=[f"${cost}" for cost in costs],
            textposition='auto',
            textfont=dict(
                color='#FFFFFF', 
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
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2c5aa0',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Cost per Day (USD)",
            title_font=dict(color='#FFFFFF', size=16, family='Inter, sans-serif'),
            tickfont=dict(color='#E5E5E5', size=12, family='Inter, sans-serif'),
            gridcolor='#2c5aa0',
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


def display_recommendation_card(rec, rank):
    """Display a single recommendation card"""
    ml_rec = rec['ml_recommendation']
    
    with st.container():
        # Professional card header
        st.markdown(f"""
        <div class="recommendation-card fade-in-up">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; 
                        border-bottom: 1px solid #333333; padding-bottom: 1rem;">
                <div style="display: flex; align-items: center;">
                    <div style="background: linear-gradient(135deg, #4a90e2 0%, #60a5fa 100%); 
                               color: #FFFFFF; width: 45px; height: 45px; border-radius: 6px; 
                               display: flex; align-items: center; justify-content: center; 
                               font-weight: 700; font-size: 1.1rem; margin-right: 1.5rem; 
                               box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);">
                        {rank}
                    </div>
                    <div>
                        <h3 style="color: #FFFFFF; margin: 0; font-weight: 600; font-size: 1.8rem; letter-spacing: -0.02em;">
                            {ml_rec['destination']}, {ml_rec['country']}
                        </h3>
                        <p style="color: #999999; margin: 0.3rem 0 0 0; font-size: 0.95rem; font-weight: 500;">
                            ML Confidence Score: <span style="color: #FFFFFF; font-weight: 600;">{rec['ml_score']:.3f}</span>
                        </p>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #999999; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em;">
                        RECOMMENDATION
                    </div>
                    <div style="color: #4a90e2; font-size: 1.5rem; font-weight: 700;">
                        #{rank}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional metrics grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{rec['ml_score']:.3f}</div>
                <div class="metric-label">ML Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">${ml_rec['cost_per_day']}</div>
                <div class="metric-label">Daily Cost</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value" style="font-size: 1.6rem;">{ml_rec['duration_range']}</div>
                <div class="metric-label">Duration</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional details section
        st.markdown(f"""
        <div class="status-card" style="margin: 1.5rem 0;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                        gap: 1rem; text-align: center;">
                <div>
                    <div style="color: #999999; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">
                        Travel Type
                    </div>
                    <div style="color: #FFFFFF; font-weight: 500; margin-top: 0.3rem;">
                        {ml_rec['trip_type'].title()}
                    </div>
                </div>
                <div>
                    <div style="color: #999999; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">
                        Region
                    </div>
                    <div style="color: #FFFFFF; font-weight: 500; margin-top: 0.3rem;">
                        {ml_rec['region']}
                    </div>
                </div>
                <div>
                    <div style="color: #999999; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">
                        Current Weather
                    </div>
                    <div style="color: #FFFFFF; font-weight: 500; margin-top: 0.3rem;">
                        {rec['weather_info'].get('current_temp', 'N/A')}°C
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional content sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Machine Learning Analysis")
            st.markdown(f"""
            <div class="content-section" style="margin: 1rem 0;">
                <p style="color: #E5E5E5; line-height: 1.6; margin: 0;">
                    {rec['ml_reasoning']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Key Attractions")
            for i, attraction in enumerate(rec['attractions'][:3], 1):
                st.markdown(f"""
                <div style="background: #16213e; border: 1px solid #4a90e2; padding: 1rem; 
                           margin: 0.5rem 0; border-radius: 6px; border-left: 3px solid #60a5fa;">
                    <div style="color: #FFFFFF; font-weight: 600;">
                        {i}. {attraction['name']}
                    </div>
                    <div style="color: #9bb5d6; font-size: 0.85rem; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;">
                        {attraction['category']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### AI-Generated Insights")
            st.markdown(f"""
            <div class="content-section" style="margin: 1rem 0;">
                <p style="color: #E5E5E5; line-height: 1.6; margin: 0;">
                    {rec['llm_explanation']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Travel Itinerary Preview")
            itinerary_preview = rec['detailed_itinerary'][:300] + "..." if len(rec['detailed_itinerary']) > 300 else rec['detailed_itinerary']
            st.markdown(f"""
            <div class="content-section" style="margin: 1rem 0;">
                <p style="color: #E5E5E5; line-height: 1.6; margin: 0; font-size: 0.9rem;">
                    {itinerary_preview}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional separator
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="TripX - AI Travel Recommendations",
        page_icon="images/tripX_logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply professional theme and initialize
    apply_professional_theme()
    initialize_session_state()
    
    # Ultra-professional TripX header - Compact Design
    
    # Executive TripX Title - Compact and Clean
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(74, 144, 226, 0.08) 0%, rgba(30, 58, 138, 0.12) 100%); border-radius: 20px; border: 1px solid rgba(74, 144, 226, 0.2);">
        <h1 style="color: #FFFFFF; font-size: 5rem; font-weight: 100; margin: 0; letter-spacing: -0.08em; text-shadow: 0 0 40px rgba(74, 144, 226, 0.4);">
            Trip<span style="color: #4a90e2; font-weight: 300;">X</span>
        </h1>
        <div style="width: 120px; height: 1px; background: #4a90e2; margin: 2rem auto; opacity: 0.8;"></div>
        <p style="color: #9bb5d6; font-size: 1.1rem; margin: 2rem 0 0 0; font-weight: 300; letter-spacing: 0.03em; line-height: 1.7;">
            Advanced Machine Learning meets Natural Language Processing<br/>
            for personalized travel recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rest of the professional header
    st.markdown("""
    <div class="professional-header fade-in-up" style="padding-top: 1rem;">
        <div style="position: relative; z-index: 2;">
            <div style="display: inline-block; padding: 1rem 2rem; border: 2px solid #4a90e2; border-radius: 50px; margin-bottom: 2rem; background: rgba(74, 144, 226, 0.1);">
                <span style="color: #60a5fa; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em;">
                    AI-Powered Travel Intelligence
                </span>
            </div>
            <div style="width: 100px; height: 3px; background: linear-gradient(90deg, #1e3a8a, #4a90e2, #60a5fa); margin: 2rem auto; border-radius: 2px;"></div>
            <p style="color: #E5E5E5; font-size: 1.4rem; margin: 1.5rem 0 0 0; font-weight: 300; letter-spacing: 0.02em; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;">
                Advanced Machine Learning meets Natural Language Processing for personalized travel recommendations
            </p>
            <div style="margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid rgba(74, 144, 226, 0.3);">
                <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
                    <div style="text-align: center;">
                        <div style="color: #4a90e2; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">320+</div>
                        <div style="color: #9bb5d6; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em;">Destinations</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #4a90e2; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">27</div>
                        <div style="color: #9bb5d6; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em;">ML Features</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #4a90e2; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">190+</div>
                        <div style="color: #9bb5d6; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em;">Countries</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main configuration section in the main page
    if st.session_state.recommendations is None:
        # Enhanced configuration section with professional styling
        st.markdown("""
        <div class="content-section fade-in-up" style="margin: 3rem 0; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 8px 32px rgba(74, 144, 226, 0.2);">
            <div style="text-align: center; margin-bottom: 3rem;">
                <div style="display: inline-block; padding: 0.5rem 1.5rem; background: var(--gradient-primary); border-radius: 25px; margin-bottom: 1.5rem;">
                    <span style="color: #FFFFFF; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em;">
                        Configure Your Journey
                    </span>
                </div>
                <h2 style="color: #FFFFFF; font-weight: 400; margin-bottom: 1rem; text-align: center; font-size: 2.2rem; letter-spacing: -0.02em;">
                    Travel Preferences
                </h2>
                <p style="color: #9bb5d6; font-size: 1rem; margin: 0 0 2rem 0; line-height: 1.6; text-align: center; max-width: 500px; margin-left: auto; margin-right: auto;">
                    Set your travel parameters and let our AI engine analyze 320+ global destinations to find your perfect match
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional configuration form
        with st.container():
            # First row - Budget and Duration
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="metric-container" style="margin-bottom: 1rem; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 4px 16px rgba(74, 144, 226, 0.15);">
                    <div style="text-align: left; padding: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                                <span style="color: #FFFFFF; font-size: 1.2rem;">💰</span>
                            </div>
                            <h4 style="color: #FFFFFF; margin: 0; font-weight: 500; font-size: 1.1rem;">Budget Range</h4>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                budget = st.number_input(
                    "Daily Budget ($)",
                    min_value=1,
                    max_value=10000,
                    value=100,
                    step=1,
                    help="Enter your maximum budget per day for accommodation, meals, and activities",
                    key="main_budget_input"
                )
                st.markdown(f"<p style='color: #9bb5d6; font-size: 0.9rem; text-align: center; margin-top: 0.5rem;'>Selected: <strong style='color: #60a5fa;'>${budget}/day</strong></p>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-container" style="margin-bottom: 1rem; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 4px 16px rgba(74, 144, 226, 0.15);">
                    <div style="text-align: left; padding: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                                <span style="color: #FFFFFF; font-size: 1.2rem;">📅</span>
                            </div>
                            <h4 style="color: #FFFFFF; margin: 0; font-weight: 500; font-size: 1.1rem;">Trip Duration</h4>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                duration = st.number_input(
                    "Trip Duration (days)",
                    min_value=1,
                    max_value=365,
                    value=7,
                    step=1,
                    help="Enter the total number of days for your travel experience",
                    key="main_duration_input"
                )
                st.markdown(f"<p style='color: #9bb5d6; font-size: 0.9rem; text-align: center; margin-top: 0.5rem;'>Selected: <strong style='color: #60a5fa;'>{duration} days</strong></p>", unsafe_allow_html=True)
            
            # Second row - Trip Type and Season
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("""
                <div class="metric-container" style="margin-bottom: 1rem; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 4px 16px rgba(74, 144, 226, 0.15);">
                    <div style="text-align: left; padding: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                                <span style="color: #FFFFFF; font-size: 1.2rem;">🎯</span>
                            </div>
                            <h4 style="color: #FFFFFF; margin: 0; font-weight: 500; font-size: 1.1rem;">Travel Style</h4>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                trip_type = st.selectbox(
                    "Trip Type",
                    options=["culture", "beach", "urban", "luxury", "nature"],
                    index=0,
                    help="Primary focus and style of your travel experience",
                    key="main_trip_type_select"
                )
            
            with col4:
                st.markdown("""
                <div class="metric-container" style="margin-bottom: 1rem; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 4px 16px rgba(74, 144, 226, 0.15);">
                    <div style="text-align: left; padding: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                                <span style="color: #FFFFFF; font-size: 1.2rem;">🌤️</span>
                            </div>
                            <h4 style="color: #FFFFFF; margin: 0; font-weight: 500; font-size: 1.1rem;">Travel Season</h4>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                season = st.selectbox(
                    "Season",
                    options=["spring", "summer", "autumn", "winter"],
                    index=0,
                    help="Preferred season for optimal weather and activities",
                    key="main_season_select"
                )
            
            # Third row - Number of recommendations (centered)
            col_left, col_center, col_right = st.columns([1, 2, 1])
            
            with col_center:
                st.markdown("""
                <div class="metric-container" style="margin-bottom: 2rem; background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 4px 16px rgba(74, 144, 226, 0.15);">
                    <div style="text-align: left; padding: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                                <span style="color: #FFFFFF; font-size: 1.2rem;">🔢</span>
                            </div>
                            <h4 style="color: #FFFFFF; margin: 0; font-weight: 500; font-size: 1.1rem;">Results Count</h4>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                num_recommendations = st.number_input(
                    "Number of Recommendations",
                    min_value=1,
                    max_value=10,
                    value=3,
                    step=1,
                    help="Type the exact number of destination recommendations you want to generate",
                    key="main_num_recs_input"
                )
                st.markdown(f"<p style='color: #9bb5d6; font-size: 0.9rem; text-align: center; margin-top: 0.5rem;'>Selected: <strong style='color: #60a5fa;'>{num_recommendations} recommendations</strong></p>", unsafe_allow_html=True)
            
            # Enhanced professional button section
            st.markdown("""
            <div style="text-align: center; margin: 3rem 0; padding: 2rem; background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(30, 58, 138, 0.1) 100%); border-radius: 15px; border: 1px solid rgba(74, 144, 226, 0.3);">
                <div style="margin-bottom: 1.5rem;">
                    <div style="color: #60a5fa; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem;">
                        Ready to Discover
                    </div>
                    <div style="color: #FFFFFF; font-size: 1.1rem; font-weight: 300;">
                        Generate personalized recommendations powered by advanced AI
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
            
            with col_btn_center:
                # Use a form with submit button for better control
                with st.form("recommendation_form"):
                    submitted = st.form_submit_button(
                        "GET AI RECOMMENDATIONS",
                        use_container_width=True,
                        help="Click to generate personalized travel recommendations"
                    )
                    
                if submitted:
                    user_preferences = {
                        "budget": budget,
                        "duration": duration,
                        "trip_type": trip_type,
                        "season": season
                    }
                    
                    st.session_state.user_preferences = user_preferences
                    
                    # Load engine and get recommendations - Backend logic unchanged
                    engine = load_engine()
                    
                    with st.spinner("🤖 AI is analyzing destinations..."):
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
                    st.rerun()
        
        # Enhanced system architecture section
        st.markdown("""
        <div style="margin: 4rem 0; text-align: center;">
            <div style="display: inline-block; padding: 0.5rem 1.5rem; background: var(--gradient-primary); border-radius: 25px; margin-bottom: 2rem;">
                <span style="color: #FFFFFF; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em;">
                    System Architecture
                </span>
            </div>
            <h3 style="color: #FFFFFF; font-weight: 400; margin-bottom: 2rem; text-align: center; font-size: 2rem; letter-spacing: -0.02em;">
                Powered by Advanced AI Technology
            </h3>
            <p style="color: #9bb5d6; font-size: 1rem; margin: 0 0 3rem 0; line-height: 1.6; text-align: center; max-width: 600px; margin-left: auto; margin-right: auto;">
                Our intelligent system combines multiple AI technologies to deliver precise, personalized travel recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional feature grid
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("""
            <div class="metric-container" style="background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 6px 20px rgba(74, 144, 226, 0.2); transform: translateY(0); transition: all 0.3s ease;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="width: 60px; height: 60px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);">
                        <span style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">ML</span>
                    </div>
                    <div class="metric-label" style="margin-bottom: 0.5rem;">Core Engine</div>
                    <div style="color: #9bb5d6; font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4;">
                        Advanced algorithms analyzing 320+ destinations with 27 engineered features
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown("""
            <div class="metric-container" style="background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 6px 20px rgba(74, 144, 226, 0.2); transform: translateY(0); transition: all 0.3s ease;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="width: 60px; height: 60px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);">
                        <span style="color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">NLP</span>
                    </div>
                    <div class="metric-label" style="margin-bottom: 0.5rem;">Language Processing</div>
                    <div style="color: #9bb5d6; font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4;">
                        Natural language generation for comprehensive travel explanations
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown("""
            <div class="metric-container" style="background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-tertiary) 100%); border: 2px solid var(--accent-color); box-shadow: 0 6px 20px rgba(74, 144, 226, 0.2); transform: translateY(0); transition: all 0.3s ease;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="width: 60px; height: 60px; background: var(--gradient-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);">
                        <span style="color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">API</span>
                    </div>
                    <div class="metric-label" style="margin-bottom: 0.5rem;">Data Integration</div>
                    <div style="color: #9bb5d6; font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4;">
                        Real-time weather and attraction data enrichment
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional system statistics
        engine = load_engine()
        if engine:
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <h3 style="color: #FFFFFF; font-weight: 500; text-align: center; margin-bottom: 2rem;">
                System Performance Metrics
            </h3>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">320+</div>
                    <div class="metric-label">Global Destinations</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">27</div>
                    <div class="metric-label">ML Features</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_c:
                st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">190+</div>
                    <div class="metric-label">Countries</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        results = st.session_state.recommendations
        
        # Back button to return to main page
        col_back_left, col_back_center, col_back_right = st.columns([1, 2, 1])
        
        with col_back_center:
            if st.button("← Back to Configuration", type="secondary", key="back_to_main_btn"):
                st.session_state.recommendations = None
                st.session_state.user_preferences = None
                st.rerun()
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        if results['status'] == 'success':
            # Display user preferences with clean styling
            prefs = st.session_state.user_preferences
            st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border-left: 3px solid #FFFFFF;">
                <strong style="color: #FFFFFF;">Your Profile:</strong> 
                <span style="color: #CCCCCC;">
                    Budget ${prefs['budget']}/day &bull; {prefs['duration']} days &bull; {prefs['trip_type']} travel &bull; {prefs['season']} season
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
                    <div style="background-color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border-left: 3px solid #FFFFFF; margin: 1rem 0;">
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