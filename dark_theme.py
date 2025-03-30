import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium
from streamlit_lottie import st_lottie
import requests

# Updated imports – using our modules for formatting and data import
from modules import importer
from modules import formater

# Set page configuration using formater module
title_obj = formater.Title()
title_obj.page_config("N3DN.Tech - Home")

# Custom CSS for basic styling - removed white background override
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #6eb52f !important;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    .card {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .filter-container {
        background: #262730;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #6eb52f !important;
    }
    
    .metric-label {
        font-size: 1rem !important;
    }
    
    /* Link styling */
    a {
        color: #8eccff !important;
        text-decoration: underline;
    }
    
    a:hover {
        color: #4da3ff !important;
    }
</style>
""", unsafe_allow_html=True)
# ---------------- Sidebar Section ----------------
# Existing top navigation (Do Not Modify)
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# All sidebar content is defined within this block.
with st.sidebar:
    # Navigation widget
    # Version information
    st.markdown("### N3DN Version: 1.0.2")

    st.markdown("---")

    # Animation section
    st.markdown("### Your Career Hub: Explore Opportunities, Skills & Insights!")
    lottie_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="sidebar_anim")
    else:
        st.error("Animation could not be loaded.")

# ---------- Sidebar Enhancements End ----------
# Main page content continues here.


# Create a session state to store our data
if 'jobs_data' not in st.session_state:
    st.session_state.jobs_data = None

# Load job data from local CSV using importer
data_file = os.path.join("data", "google_jobs.csv")
if os.path.exists(data_file) and st.session_state.jobs_data is None:
    st.session_state.jobs_data = importer.DataImport.fetch_and_clean_data(max_rows=1000)
else:
    st.session_state.jobs_data = importer.DataImport.fetch_and_clean_data(max_rows=1000)

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p style="font-size: 3.0rem; font-weight: bold; color: #6eb52f;">Welcome to N3DN.Tech</p>', unsafe_allow_html=True)

    st.markdown('<p class="sub-header">Data-Driven Insights for Technology Professionals</p>', unsafe_allow_html=True)
with col2:
    st.markdown(f"<h3>Data Updated: {datetime.now().year}</h3>", unsafe_allow_html=True)

# App Overview Section
st.title("N3DN.Tech - Tech Career Analytics Platform")
st.write("""
N3DN.Tech helps technology professionals make data-driven career decisions by providing comprehensive 
analytics on the job market, in-demand skills, and salary trends.
""")
st.subheader("Key Features")
st.markdown("""
<table>
    <tr>
        <th>Feature</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>📊 Job Data Insights</td>
        <td>Analyze job market trends using pre-fetched data from our trusted source.</td>
    </tr>
    <tr>
        <td>🔍 Skills Analysis</td>
        <td>Identify the most in-demand skills for tech professionals.</td>
    </tr>
    <tr>
        <td>💰 Salary Insights</td>
        <td>Track compensation trends across various roles and experience levels.</td>
    </tr>
    <tr>
        <td>🤖 Career Advisor</td>
        <td>Receive recommendations based on your profile and job market data.</td>
    </tr>
    <tr>
        <td>📈 Interactive Visualizations</td>
        <td>Explore trends and patterns through intuitive charts and maps.</td>
    </tr>
</table>
""", unsafe_allow_html=True)
st.info("""
**How to Get Started:**

- Begin with the **Top Skills** page to discover which technologies are most in demand.
- Next, explore **Skill Trends** to see how these demands are evolving over time.
- Then check **Skills vs Pay** to understand which skills lead to higher compensation.
- Finally, use the **Career Advisor** for personalized guidance based on your goals.
""")

# Key Metrics Section
st.markdown("### Key Insights")
col1_metric, col2_metric, col3_metric, col4_metric = st.columns(4)

trending_topic_display = "Data Analysis"
avg_salary_display = "$145K"
top_skill_display = "Python"
yoy_growth_display = "+24%"


if st.session_state.jobs_data is not None:
    if 'salary_yearly' in st.session_state.jobs_data.columns:
        salary_data = st.session_state.jobs_data['salary_yearly'].dropna()
        if not salary_data.empty:
            avg_salary_display = f"${int(salary_data.mean() / 1000)}K"
    elif 'salary' in st.session_state.jobs_data.columns:
        salary_data = st.session_state.jobs_data['salary'].dropna()
        if not salary_data.empty:
            avg_salary_display = f"${int(salary_data.mean() / 1000)}K"
    if 'description_tokens' in st.session_state.jobs_data.columns:
        all_skills = []
        for tokens in st.session_state.jobs_data['description_tokens'].dropna():
            if isinstance(tokens, str):
                skills = tokens.strip("[]").replace("'", "").split(", ")
                all_skills.extend(skills)
        skill_counts = pd.Series(all_skills).value_counts()
        if not skill_counts.empty:
            top_skill_display = skill_counts.index[0]
            if 'posted_at' in st.session_state.jobs_data.columns:
                try:
                    st.session_state.jobs_data['posted_date'] = pd.to_datetime(
                        st.session_state.jobs_data['posted_at'], errors='coerce'
                    )
                    recent_date = st.session_state.jobs_data['posted_date'].max() - pd.Timedelta(days=90)
                    recent_jobs = st.session_state.jobs_data[st.session_state.jobs_data['posted_date'] >= recent_date]
                    if not recent_jobs.empty and 'description_tokens' in recent_jobs.columns:
                        recent_skills = []
                        for tokens in recent_jobs['description_tokens'].dropna():
                            if isinstance(tokens, str):
                                skills = tokens.strip("[]").replace("'", "").split(", ")
                                recent_skills.extend(skills)
                        recent_skill_counts = pd.Series(recent_skills).value_counts()
                        if not recent_skill_counts.empty:
                            trending_topic_display = recent_skill_counts.index[0]
                except Exception as e:
                    pass

with col1_metric:
    st.markdown(f'<div class="card"><p class="metric-value">{avg_salary_display}</p><p class="metric-label">Average Salary</p></div>', unsafe_allow_html=True)
with col2_metric:
    st.markdown(f'<div class="card"><p class="metric-value">{top_skill_display}</p><p class="metric-label">Top Skill</p></div>', unsafe_allow_html=True)
with col3_metric:
    st.markdown(f'<div class="card"><p class="metric-value">{yoy_growth_display}</p><p class="metric-label">YoY Growth</p></div>', unsafe_allow_html=True)
with col4_metric:
    st.markdown(f'<div class="card"><p class="metric-value">{trending_topic_display}</p><p class="metric-label">Trending Topic</p></div>', unsafe_allow_html=True)

# Main Content Description
st.markdown("### Explore Our Data")
st.markdown("""
This interactive dashboard provides comprehensive insights into the job market for technology professionals:

- **Top Skills**: Discover the most in-demand skills for tech professionals.
- **Skill Trends**: Track emerging technologies and skills in the tech space.
- **Skills vs. Pay**: Analyze which skills correlate with higher compensation.
- **Career Advisor**: Get personalized recommendations based on your profile and market trends.
- **About**: Learn more about our data collection methodology and mission.
""", unsafe_allow_html=True)

# Stay Updated section
st.markdown("### Stay Updated")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### Connect With Us")
st.markdown("""
[YouTube](https://www.youtube.com/watch?si=gOpctWkfOWA8f9v_&v=43PzmabhZL0&feature=youtu.be) | 
[GitHub](https://github.com/Shwetanlondhe24/HM0043_Team-Neural-Net-Ninjas)
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2025 N3DN.Tech. All data is for demonstration purposes only.</div>', unsafe_allow_html=True) 