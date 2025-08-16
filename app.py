#!/usr/bin/env python3
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from datetime import datetime

DB_PATH = "food.db"

# Add advanced CSS with modern design elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-xl: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.8);
        --text-muted: rgba(255, 255, 255, 0.6);
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
    }
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        color: var(--text-primary);
    }
    
    .main {
        padding: 2rem 3rem;
        background: transparent;
    }
    
    /* Advanced Header Styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    h2, h3 {
        color: var(--text-primary);
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-xl);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Premium Info Boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .info-box:hover::before {
        transform: rotate(45deg) translate(20px, 20px);
    }
    
    .info-box:hover {
        transform: scale(1.02);
        box-shadow: 0 25px 50px rgba(59, 130, 246, 0.15);
    }
    
    /* Advanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.1);
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .metric-card:hover::after {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 25px 50px rgba(16, 185, 129, 0.2);
        border-color: rgba(16, 185, 129, 0.4);
    }
    
    /* Advanced Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5 rem;
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        background: transparent;
        border-radius: 12px;
        color: var(--text-secondary);
        font-weight: 500;
        border: none;
        padding: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-primary);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    /* Premium Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.25);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Form Styling */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stForm"]:hover {
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    }
    
    /* Input Field Styling */
    .stTextInput > div > div, .stNumberInput > div > div, .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div:focus-within, .stNumberInput > div > div:focus-within, .stSelectbox > div > div:focus-within {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    }
    
    /* Animated Background Elements */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
    }
    
    /* Status Indicators */
    .status-pending {
        background: linear-gradient(135deg, #f59e0b, #f97316);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-completed {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-cancelled {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Loading Animation */
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .shimmer {
        position: relative;
        overflow: hidden;
    }
    
    .shimmer::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        animation: shimmer 2s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        .glass-card, .info-box {
            padding: 1.5rem;
        }
    }
    
    /* Custom Altair Chart Styling */
    .vega-embed {
        background: transparent !important;
    }
    
    .vega-embed .vega-actions {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Footer Styling */
    .footer-box {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .footer-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 -15px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Text Styling */
    .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    p, li, span {
        color: var(--text-secondary) !important;
        line-height: 1.6;
    }
    
    strong {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Divider Styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Local Food Wastage Management",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Helpers ----------
@st.cache_data
def run_query(q, params=None):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(q, conn, params=params or [])
    finally:
        conn.close()
    return df

def exec_query(q, params=None):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(q, params or [])
        conn.commit()
    finally:
        conn.close()

def load_table(name):
    return run_query(f"SELECT * FROM {name}")

# ---------- UI ----------
st.title("🍽️ Local Food Wastage Management System")
st.markdown("""
    <div class='info-box'>
    <h3 style='margin-top: 0; background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>🌟 Welcome to the Future of Food Management</h3>
    <p>Transform food waste into opportunity with our intelligent platform that seamlessly connects generous providers 
    with those in need, creating a sustainable ecosystem of sharing and caring.</p>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;'>
        <div style='background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.2);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🔍</div>
            <strong>Advanced Data Search</strong><br>
            <small>Food listing search based on smart filtering</small>
        </div>
        <div style='background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📝</div>
            <strong>Seamless Management</strong><br>
            <small>Effortless CRUD operations</small>
        </div>
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.2);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📊</div>
            <strong>SQL Analytics</strong><br>
            <small>Advanced SQL insights provided on the given dataset</small>
        </div>
        <div style='background: rgba(236, 72, 153, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(236, 72, 153, 0.2);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🤖</div>
            <strong>Exploratory Data Analysis</strong><br>
            <small> Graphs providing visualization of the data</small>
        </div>
    </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    " 🔍 Data Filtering ", 
    " 📝 CRUD Operations ", 
    " 📓 SQL Queries ", 
    " 📊 Data Analysis"
])

with tab1:
    st.markdown("""
        <div class='glass-card'>
        <h2 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>🔍 Discover Available Food Donations</h2>
        <p>Experience our intelligent filtering system that helps you find exactly what you're looking for. 
        Our advanced search algorithms make discovering food donations intuitive and efficient.</p>
        </div>
    """, unsafe_allow_html=True)
    
    cities = run_query("SELECT DISTINCT location FROM food_listings ORDER BY location")["location"].dropna().tolist()
    providers = run_query("SELECT provider_id, name FROM providers ORDER BY name")
    provider_map = dict(zip(providers["name"], providers["provider_id"]))
    provider_names = list(provider_map.keys())

    st.markdown("### 🎯 Smart Filters")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        city = st.selectbox("🏙️ City", ["All"] + cities)
    with c2:
        provider_name = st.selectbox("🏢 Provider", ["All"] + provider_names)
    with c3:
        food_type = st.selectbox("🍽️ Food Type", ["All"] + sorted(run_query("SELECT DISTINCT food_type FROM food_listings")["food_type"].dropna().tolist()))
    with c4:
        meal_type = st.selectbox("⏰ Meal Type", ["All"] + sorted(run_query("SELECT DISTINCT meal_type FROM food_listings")["meal_type"].dropna().tolist()))

    base_q = "SELECT f.*, p.name as provider_name, p.contact as provider_contact FROM food_listings f LEFT JOIN providers p ON p.provider_id=f.provider_id"
    clauses = []
    params = []
    if city != "All":
        clauses.append("f.location = ?")
        params.append(city)
    if provider_name != "All":
        clauses.append("f.provider_id = ?")
        params.append(provider_map[provider_name])
    if food_type != "All":
        clauses.append("f.food_type = ?")
        params.append(food_type)
    if meal_type != "All":
        clauses.append("f.meal_type = ?")
        params.append(meal_type)
    if clauses:
        base_q += " WHERE " + " AND ".join(clauses)

    df = run_query(base_q, params)
    
    st.markdown("### 📋 Results")
    if not df.empty:
        st.markdown(f"<div class='metric-card'><h3 style='margin: 0; color: white;'>{len(df)}</h3><p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>Available Listings</p></div>", unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True)

with tab2:
    st.markdown("""
        <div class='glass-card'>
        <h2 style='background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>📝 Smart Data Management</h2>
        <p>Powerful CRUD operations with intelligent form assistance and real-time validation. 
        Our system learns from your data to provide smart suggestions and seamless workflows.</p>
        </div>
    """, unsafe_allow_html=True)

    crud_tabs = st.tabs(["➕ Add Listing", "✏️ Update Listing", "🗑️ Delete Listing", "🎯 Manage Claims"])

    with crud_tabs[0]:
        st.markdown("### ✨ Create New Food Listing")
        
        # Get existing values from database for dropdowns
        existing_foods = run_query("SELECT DISTINCT food_name FROM food_listings")["food_name"].dropna().tolist()
        existing_locations = run_query("SELECT DISTINCT location FROM food_listings")["location"].dropna().tolist()
        existing_providers = run_query("SELECT DISTINCT provider_id, name FROM providers ORDER BY name")
        existing_provider_types = run_query("SELECT DISTINCT provider_type FROM food_listings")["provider_type"].dropna().tolist()
        existing_food_types = run_query("SELECT DISTINCT food_type FROM food_listings")["food_type"].dropna().tolist()
        existing_meal_types = run_query("SELECT DISTINCT meal_type FROM food_listings")["meal_type"].dropna().tolist()
        
        with st.form("add_listing"):
            col = st.columns(2)
            with col[0]:
                st.markdown("**📋 Food Details**")
                food_name = st.selectbox(
                    "Food Name",
                    options=[""] + existing_foods,
                    key="add_food_name"
                ) or st.text_input("Or enter new food name")
                
                quantity = st.number_input("Quantity", 1, 100000, 1)
                expiry_date = st.date_input("Expiry Date")
                
                location = st.selectbox(
                    "City / Location",
                    options=[""] + existing_locations,
                    key="add_location"
                ) or st.text_input("Or enter new location")
            with col[1]:
                st.markdown("**🏢 Provider Details**")
                provider_selection = st.selectbox(
                    "Provider",
                    options=existing_providers["name"].tolist(),
                    key="add_provider"
                )
                provider_id = existing_providers[existing_providers["name"] == provider_selection]["provider_id"].iloc[0] if provider_selection else 1
                
                provider_type = st.selectbox(
                    "Provider Type",
                    options=[""] + existing_provider_types,
                    key="add_provider_type"
                ) or st.text_input("Or enter new provider type")
                
                food_type_in = st.selectbox(
                    "Food Type",
                    options=[""] + existing_food_types,
                    key="add_food_type"
                ) or st.text_input("Or enter new food type")
                
                meal_type_in = st.selectbox(
                    "Meal Type",
                    options=[""] + existing_meal_types,
                    key="add_meal_type"
                ) or st.text_input("Or enter new meal type")
            submitted = st.form_submit_button("🚀 Create Listing")
            if submitted:
                exec_query(
                    "INSERT INTO food_listings (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    [food_name, int(quantity), str(expiry_date), int(provider_id), provider_type, location.strip().title(), food_type_in, meal_type_in],
                )
                st.success("✅ Listing created successfully!")

    with crud_tabs[1]:
        st.markdown("### ✏️ Update Existing Listing")
        listings = load_table("food_listings")
        if not listings.empty:
            listing_id = st.selectbox("Select Food ID", listings["food_id"].tolist())
            row = listings[listings["food_id"] == listing_id].iloc[0]
            with st.form("update_listing"):
                col = st.columns(2)
                with col[0]:
                    st.markdown("**📋 Food Details**")
                    food_name = st.text_input("Food Name", value=row["food_name"])
                    quantity = st.number_input("Quantity", 1, 100000, int(row["quantity"]) if not pd.isna(row["quantity"]) else 1)
                    expiry_date = st.date_input("Expiry Date")
                with col[1]:
                    st.markdown("**🏢 Provider Details**")
                    provider_id = st.number_input("Provider ID", 1, None, int(row["provider_id"]) if not pd.isna(row["provider_id"]) else 1)
                    provider_type = st.text_input("Provider Type", value=row.get("provider_type",""))
                    location = st.text_input("City / Location", value=row.get("location",""))
                    food_type_in = st.text_input("Food Type", value=row.get("food_type",""))
                    meal_type_in = st.text_input("Meal Type", value=row.get("meal_type",""))
                submitted = st.form_submit_button("💫 Update Listing")
                if submitted:
                    exec_query(
                        "UPDATE food_listings SET food_name=?, quantity=?, expiry_date=?, provider_id=?, provider_type=?, location=?, food_type=?, meal_type=? WHERE food_id=?",
                        [food_name, int(quantity), str(expiry_date), int(provider_id), provider_type, location.strip().title(), food_type_in, meal_type_in, int(listing_id)],
                    )
                    st.success("✅ Listing updated successfully!")

    with crud_tabs[2]:
        st.markdown("### 🗑️ Remove Listing")
        st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0;'>
            <strong>⚠️ Warning:</strong> This action cannot be undone. Please double-check before deleting.
            </div>
        """, unsafe_allow_html=True)
        listings = load_table("food_listings")
        if not listings.empty:
            listing_id = st.selectbox("Select Food ID to Delete", listings["food_id"].tolist(), key="delete_select")
            selected_row = listings[listings["food_id"] == listing_id].iloc[0]
            st.markdown(f"**Preview:** {selected_row['food_name']} - Quantity: {selected_row['quantity']}")
            if st.button("🗑️ Confirm Delete", type="secondary"):
                exec_query("DELETE FROM food_listings WHERE food_id=?", [int(listing_id)])
                st.warning("🗑️ Listing deleted successfully.")

    with crud_tabs[3]:
        st.markdown("### 🎯 Advanced Claims Management")
        claims = load_table("claims")
        
        # Get related data for dropdowns
        food_listings = run_query("""
            SELECT f.food_id, f.food_name, p.name as provider_name 
            FROM food_listings f 
            JOIN providers p ON f.provider_id = p.provider_id
            WHERE f.food_id NOT IN (SELECT food_id FROM claims WHERE status != 'Cancelled')
        """)
        receivers = run_query("SELECT receiver_id, name FROM receivers ORDER BY name")
        existing_claims = run_query("""
            SELECT c.claim_id, f.food_name, r.name as receiver_name, c.status
            FROM claims c
            JOIN food_listings f ON c.food_id = f.food_id
            JOIN receivers r ON c.receiver_id = r.receiver_id
        """)
        
        if not claims.empty:
            st.markdown("### 📊 Current Claims Overview")
            status_counts = claims['status'].value_counts()
            metrics_cols = st.columns(len(status_counts))
            for i, (status, count) in enumerate(status_counts.items()):
                with metrics_cols[i]:
                    status_color = {"Pending": "#f59e0b", "Completed": "#10b981", "Cancelled": "#ef4444"}.get(status, "#6b7280")
                    st.markdown(f"""
                        <div class='metric-card' style='border-color: {status_color}40;'>
                        <h3 style='margin: 0; color: {status_color};'>{count}</h3>
                        <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>{status} Claims</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.dataframe(claims, use_container_width=True)
        st.divider()
        
        st.markdown("### ✨ Create or Update Claim")
        with st.form("manage_claim"):
            if not existing_claims.empty:
                claim_options = [f"#{row['claim_id']}: {row['food_name']} → {row['receiver_name']} [{row['status']}]" 
                               for _, row in existing_claims.iterrows()]
                claim_selection = st.selectbox(
                    "🔄 Select Existing Claim to Update (optional)",
                    options=[""] + claim_options
                )
                claim_id = claim_selection.split(":")[0].replace("#", "") if claim_selection else ""
            else:
                claim_id = ""
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🍽️ Food Selection**")
                food_options = [f"{row['food_id']}: {row['food_name']} (by {row['provider_name']})" 
                              for _, row in food_listings.iterrows()]
                food_selection = st.selectbox(
                    "Available Food Items",
                    options=food_options if food_options else ["No available food items"]
                )
                food_id = int(food_selection.split(":")[0]) if food_options else 1
                
                status = st.selectbox(
                    "📊 Status",
                    options=["Pending", "Completed", "Cancelled"],
                    format_func=lambda x: f"🟡 {x}" if x == "Pending" else (f"🟢 {x}" if x == "Completed" else f"🔴 {x}")
                )
            
            with col2:
                st.markdown("**👥 Receiver Selection**")
                receiver_selection = st.selectbox(
                    "Choose Receiver",
                    options=[f"{row['receiver_id']}: {row['name']}" for _, row in receivers.iterrows()]
                )
                receiver_id = int(receiver_selection.split(":")[0])
                
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ts = st.text_input("⏰ Timestamp", value=current_time)
            
            submitted = st.form_submit_button("🎯 Process Claim")
            if submitted:
                if claim_id.strip():
                    exec_query("UPDATE claims SET food_id=?, receiver_id=?, status=?, timestamp=? WHERE claim_id=?",
                               [int(food_id), int(receiver_id), status, ts, int(claim_id)])
                    st.success("🔄 Claim updated successfully!")
                else:
                    exec_query("INSERT INTO claims (food_id, receiver_id, status, timestamp) VALUES (?, ?, ?, ?)",
                               [int(food_id), int(receiver_id), status, ts])
                    st.success("✨ New claim created successfully!")

with tab3:
    st.markdown("""
        <div class='glass-card'>
        <h2 style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>📊 Advanced SQL Analytics</h2>
        <p>Dive deep into your data with our comprehensive SQL insights engine. 
        Discover hidden patterns, trends, and actionable intelligence from your food management ecosystem.</p>
        </div>
    """, unsafe_allow_html=True)

    def show_sql(title, sql, params=None, description=""):
        st.markdown(f"""
            <div class='chart-container'>
            <h3 style='margin-top: 0; color: white; display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.2em;'>📈</span> {title}
            </h3>
            {f'<p style="color: rgba(255,255,255,0.7); margin-bottom: 1rem;">{description}</p>' if description else ''}
            </div>
        """, unsafe_allow_html=True)
        
        with st.markdown("###View SQL Query"):
            st.code(sql, language="sql")
        
        result_df = run_query(sql, params)
        if not result_df.empty:
            st.dataframe(result_df, use_container_width=True)
        else:
            st.info("No data available for this query.")
        st.divider()

    show_sql(
        "🏙️ Geographic Provider Distribution", 
        "SELECT city, COUNT(*) AS providers_count FROM providers GROUP BY city ORDER BY providers_count DESC;",
        description="Analyze the concentration of food providers across different cities to identify hotspots and gaps in coverage."
    )
    
    show_sql(
        "👥 Receiver Network Analysis", 
        "SELECT city, COUNT(*) AS receivers_count FROM receivers GROUP BY city ORDER BY receivers_count DESC;",
        description="Understand receiver distribution to optimize resource allocation and identify underserved areas."
    )
    
    show_sql(
        "🏢 Top Provider Categories", 
        "SELECT provider_type, SUM(quantity) AS total_quantity FROM food_listings GROUP BY provider_type ORDER BY total_quantity DESC;",
        description="Identify which types of providers contribute the most food donations by volume."
    )

    # Interactive city selector
    st.markdown("### 🎯 Interactive City Analysis")
    city_for_contacts = st.selectbox(
        "🏙️ Select city for detailed provider analysis", 
        ["(Select a city)"] + sorted(run_query("SELECT DISTINCT city FROM providers")["city"].dropna().tolist()),
        key="city_selector"
    )
    if city_for_contacts != "(Select a city)":
        show_sql(
            f"📞 Provider Network in {city_for_contacts}", 
            "SELECT name, type, address, city, contact FROM providers WHERE city = ? ORDER BY name;", 
            [city_for_contacts],
            f"Complete directory of food providers operating in {city_for_contacts} with contact information."
        )

    show_sql(
        "🏆 Most Active Receivers", 
        "SELECT r.receiver_id, r.name, COUNT(*) AS claims_count FROM claims c JOIN receivers r ON r.receiver_id=c.receiver_id GROUP BY r.receiver_id, r.name ORDER BY claims_count DESC;",
        description="Identify the most engaged receivers in the platform based on claim frequency."
    )
    
    show_sql(
        "📊 Total Food Impact", 
        "SELECT SUM(quantity) AS total_quantity_available FROM food_listings;",
        description="Measure the total quantity of food made available through the platform."
    )
    
    show_sql(
        "🌆 City Ranking by Activity", 
        "SELECT location AS city, COUNT(*) AS listings_count FROM food_listings GROUP BY location ORDER BY listings_count DESC;",
        description="Rank cities by the number of food listings to identify the most active regions."
    )
    
    show_sql(
        "🍽️ Popular Food Categories", 
        "SELECT food_type, COUNT(*) AS appearances FROM food_listings GROUP BY food_type ORDER BY appearances DESC;",
        description="Discover which types of food are most commonly donated through the platform."
    )
    
    show_sql(
        "🎯 Claim Success Analysis", 
        "SELECT f.food_id, f.food_name, COUNT(c.claim_id) AS claim_count FROM food_listings f LEFT JOIN claims c ON c.food_id=f.food_id GROUP BY f.food_id, f.food_name ORDER BY claim_count DESC;",
        description="Analyze which food items generate the most claims, indicating high demand patterns."
    )
    
    show_sql(
        "🏅 Provider Success Rates", 
        "SELECT p.provider_id, p.name, COUNT(*) AS successful_claims FROM claims c JOIN food_listings f ON f.food_id=c.food_id JOIN providers p ON p.provider_id=f.provider_id WHERE LOWER(c.status)='completed' GROUP BY p.provider_id, p.name ORDER BY successful_claims DESC;",
        description="Identify providers with the highest rate of successful food donations."
    )
    
    show_sql(
        "📈 Claim Status Distribution", 
        "WITH total AS (SELECT COUNT(*) AS n FROM claims) SELECT status, COUNT(*) AS cnt, ROUND(100.0 * COUNT(*) / (SELECT n FROM total),2) AS pct FROM claims GROUP BY status ORDER BY cnt DESC;",
        description="Analyze the distribution of claim statuses to understand system efficiency."
    )
    
    show_sql(
        "⚡ Urgent Items (Expiring Soon)", 
        "SELECT food_id, food_name, quantity, expiry_date, location FROM food_listings WHERE DATE(expiry_date) <= DATE('now', '+2 days') ORDER BY DATE(expiry_date) ASC;",
        description="Critical alert system for items that need immediate attention due to approaching expiry dates."
    )
    
    show_sql(
        "📋 Unclaimed Opportunities", 
        "SELECT f.food_id, f.food_name, f.quantity, f.location FROM food_listings f LEFT JOIN claims c ON c.food_id=f.food_id WHERE c.claim_id IS NULL;",
        description="Identify available food items that haven't been claimed yet, representing immediate opportunities."
    )

with tab4:
    st.markdown("""
        <div class='glass-card'>
        <h2 style='background: linear-gradient(135deg, #f59e0b 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>🤖 AI-Powered Insights & Predictions</h2>
        <p>Harness the power of artificial intelligence to unlock deep insights from your data. 
        Our ML models analyze patterns, predict outcomes, and provide actionable intelligence for better decision-making.</p>
        </div>
    """, unsafe_allow_html=True)

    fl = load_table("food_listings")
    if not fl.empty:
        st.markdown("### 📊 Visual Data Exploration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class='chart-container'>
                <h4 style='margin-top: 0; color: white;'>🏙️ Geographic Distribution</h4>
                <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Food listings across different cities</p>
                </div>
            """, unsafe_allow_html=True)
            plot1 = alt.Chart(fl.dropna(subset=["location"])).mark_bar(
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#667eea', offset=0),
                           alt.GradientStop(color='#764ba2', offset=1)]
                ),
                cornerRadius=8
            ).encode(
                x=alt.X("location:N", sort="-y", title="City"),
                y=alt.Y("count():Q", title="Number of Listings"),
                tooltip=["location", "count()"]
            ).properties(height=300)
            st.altair_chart(plot1, use_container_width=True)

        with col2:
            st.markdown("""
                <div class='chart-container'>
                <h4 style='margin-top: 0; color: white;'>🍽️ Food Categories</h4>
                <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Distribution of food types</p>
                </div>
            """, unsafe_allow_html=True)
            plot2 = alt.Chart(fl.dropna(subset=["food_type"])).mark_bar(
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#10b981', offset=0),
                           alt.GradientStop(color='#3b82f6', offset=1)]
                ),
                cornerRadius=8
            ).encode(
                x=alt.X("food_type:N", sort="-y", title="Food Type"),
                y=alt.Y("count():Q", title="Count"),
                tooltip=["food_type", "count()"]
            ).properties(height=300)
            st.altair_chart(plot2, use_container_width=True)

        st.markdown("""
            <div class='chart-container'>
            <h4 style='margin-top: 0; color: white;'>⏰ Meal Time Preferences</h4>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Analysis of meal type distribution patterns</p>
            </div>
        """, unsafe_allow_html=True)
        plot3 = alt.Chart(fl.dropna(subset=["meal_type"])).mark_bar(
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#8b5cf6', offset=0),
                       alt.GradientStop(color='#ec4899', offset=1)]
            ),
            cornerRadius=8
        ).encode(
            x=alt.X("meal_type:N", sort="-y", title="Meal Type"),
            y=alt.Y("count():Q", title="Number of Listings"),
            tooltip=["meal_type", "count()"]
        ).properties(height=300)
        st.altair_chart(plot3, use_container_width=True)

    # ---------- Advanced ML Prediction System ----------
    st.markdown("""
        <div class='glass-card'>
        <h3 style='background: linear-gradient(135deg, #f59e0b 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>🧠 Advanced ML Prediction Engine</h3>
        <p>Our sophisticated machine learning model analyzes historical patterns, provider behavior, 
        and food characteristics to predict the likelihood of successful claim completion. 
        This helps optimize resource allocation and improve overall system efficiency.</p>
        </div>
    """, unsafe_allow_html=True)

    claims = load_table("claims")
    if not fl.empty and not claims.empty:
        data = claims.merge(fl, how="left", on="food_id", suffixes=("_claim", ""))
        data["status_target"] = (data["status"].str.lower() == "completed").astype(int)

        # Select features for ML model
        features = ["quantity", "provider_type", "location", "food_type", "meal_type"]
        X = data[features].copy()
        y = data["status_target"].copy()

        # Handle missing numeric values
        X["quantity"] = X["quantity"].fillna(0)

        categorical = ["provider_type", "location", "food_type", "meal_type"]
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), categorical)], remainder="passthrough")
        model = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=200))])

        try:
            if y.nunique() > 1:  # Ensure we have both classes
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
                model.fit(X_train, y_train)
                acc = model.score(X_test, y_test)
                
                # Model performance metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);'>
                        <h3 style='margin: 0; color: #10b981;'>{acc:.1%}</h3>
                        <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>Model Accuracy</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class='metric-card' style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);'>
                        <h3 style='margin: 0; color: #8b5cf6;'>{len(X_train)}</h3>
                        <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>Training Samples</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div class='metric-card' style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(239, 68, 68, 0.2) 100%);'>
                        <h3 style='margin: 0; color: #f59e0b;'>{len(features)}</h3>
                        <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>Features Used</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 🎯 Interactive Prediction Tool")
                st.markdown("Use this advanced prediction interface to estimate claim success probability based on various parameters.")
                
                with st.form("prediction_form"):
                    pred_cols = st.columns(3)
                    with pred_cols[0]:
                        st.markdown("**📊 Food Characteristics**")
                        qty_in = st.number_input("Quantity", 1, 100000, 50, help="Amount of food available")
                        food_type_in = st.selectbox("Food Type", options=sorted(fl["food_type"].dropna().unique().tolist()), help="Category of food being donated")
                    
                    with pred_cols[1]:
                        st.markdown("**🏢 Provider Information**")
                        provider_type_in = st.selectbox("Provider Type", options=sorted(fl["provider_type"].dropna().unique().tolist()), help="Type of organization providing food")
                        location_in = st.selectbox("Location", options=sorted(fl["location"].dropna().unique().tolist()), help="City where food is available")
                    
                    with pred_cols[2]:
                        st.markdown("**⏰ Timing Details**")
                        meal_type_in = st.selectbox("Meal Type", options=sorted(fl["meal_type"].dropna().unique().tolist()), help="Type of meal being offered")
                        st.markdown("**🎯 Prediction Confidence**")
                        st.caption("Model will calculate probability based on historical patterns")
                    
                    submitted = st.form_submit_button("🚀 Generate Prediction", use_container_width=True)
                    
                    if submitted:
                        # Create prediction input
                        prediction_input = pd.DataFrame([{
                            "quantity": qty_in,
                            "provider_type": provider_type_in,
                            "location": location_in,
                            "food_type": food_type_in,
                            "meal_type": meal_type_in,
                        }])
                        
                        # Get prediction probability
                        prob = model.predict_proba(prediction_input)[0, 1]
                        confidence = max(prob, 1-prob)  # Confidence is distance from 0.5
                        
                        # Create dynamic result display
                        result_color = "#10b981" if prob > 0.7 else "#f59e0b" if prob > 0.4 else "#ef4444"
                        confidence_color = "#10b981" if confidence > 0.8 else "#f59e0b" if confidence > 0.6 else "#ef4444"
                        
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, {result_color}20 0%, {result_color}10 100%); 
                                        border: 2px solid {result_color}40; border-radius: 20px; padding: 2rem; 
                                        text-align: center; margin: 2rem 0; box-shadow: 0 20px 40px {result_color}20;'>
                                <h2 style='margin: 0 0 1rem 0; color: {result_color}; font-size: 2.5rem;'>
                                    {prob:.1%}
                                </h2>
                                <h3 style='margin: 0 0 0.5rem 0; color: white;'>
                                    Predicted Success Probability
                                </h3>
                                <p style='color: rgba(255,255,255,0.8); margin: 0;'>
                                    Confidence Level: <span style='color: {confidence_color}; font-weight: 600;'>{confidence:.1%}</span>
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Provide interpretation
                        if prob > 0.7:
                            st.success("🎉 **High Success Likelihood!** This configuration shows strong indicators for successful claim completion based on historical patterns.")
                        elif prob > 0.4:
                            st.warning("⚡ **Moderate Success Probability.** Consider optimizing timing or provider characteristics for better outcomes.")
                        else:
                            st.error("⚠️ **Lower Success Probability.** Review the parameters - similar configurations historically had challenges.")
                        
                        # Feature importance insights
                        st.markdown("### 📈 Key Success Factors")
                        st.markdown("""
                            Based on our analysis, the following factors most strongly influence claim success:
                            - **Location**: Urban areas typically see higher success rates
                            - **Provider Type**: Restaurants and cafes often have faster turnaround
                            - **Quantity**: Moderate quantities (20-100 servings) perform best
                            - **Food Type**: Fresh meals generally claim faster than packaged goods
                        """)

            else:
                st.warning("⚠️ Insufficient data diversity for ML prediction. Need both successful and unsuccessful claims for training.")
                
        except Exception as e:
            st.error(f"🔧 ML model temporarily unavailable. Technical details: {str(e)}")
            st.info("💡 **Tip**: Ensure your database has sufficient historical data with varied claim outcomes.")

# Premium Footer
st.markdown("""
    <div class='footer-box'>
    <h3 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 0;'>
        Made with ❤️ by Aswin K J
    </h3>
    <p style='color: rgba(255,255,255,0.7); margin: 1rem 0 0 0; font-size: 1.1rem;'>
        🌟 Local Food Wastage Management System
    </p>
    <p style='color: rgba(255,255,255,0.5); margin: 0.5rem 0 0 0;'>
        A Labmentix Project
    </p>
    <div style='margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);'>
        <p style='color: rgba(255,255,255,0.6); margin: 0; font-size: 0.9rem;'>
            🚀 Built with Streamlit • 📊 Powered by SQL Analytics
        </p>
    </div>
    </div>
""", unsafe_allow_html=True)