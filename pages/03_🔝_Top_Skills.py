import streamlit as st
from modules import formater  # Page formatting module

# Set page config first - must be the first streamlit command
title_obj = formater.Title()
title_obj.page_config("N3DN.Tech - Top Skills")

import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime
from collections import Counter
import re
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests


from modules import importer  # Data import module

# ---------- CONFIGURATION ----------
load_dotenv()
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GENAI_API_KEY:
    st.error("Google API key not found in .env file.")
genai.configure(api_key=GENAI_API_KEY)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Title styles */
    .page-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #6eb52f !important;
        margin-bottom: 1rem !important;
    }
    
    .section-header {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Card styling */
    .card, .metric-card, .insight-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    
    /* Filter container */
    .filter-container {
        background: #262730;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2.2rem !important;
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
    
    /* Table styling */
    .skills-table {
        width: 100%;
        margin-top: 15px;
    }
    
    .skills-table th {
        background-color: #262730;
        color: white;
        padding: 8px;
        border-bottom: 2px solid #444;
    }
    
    .skills-table td {
        padding: 8px;
        border-bottom: 1px solid #444;
    }
    
    .skills-table tr:hover {
        background-color: #303340;
    }
</style>
""", unsafe_allow_html=True)
#--------------SIDE BAR ANIMATION0---------------------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

with st.sidebar:
    # Navigation widget for your top pages

    # Animation section for a "top" or "reaching new heights" theme
    st.markdown("### Unlock Your Potential: Discover the Top Skills in Demand!")
    # Using a different Lottie animation URL (feel free to replace this URL with another if needed)
    lottie_animation = load_lottie_url("https://lottie.host/24a9d74c-0102-4abb-b1ef-967e962d9bee/B9iFXML8x0.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="top_anim")
    else:
        st.error("Animation could not be loaded.")

#-------------END HERE---------------------------------

# ---------- DATA LOADING ----------
def load_jobs_data():
    if 'jobs_data' in st.session_state and st.session_state.jobs_data is not None:
        return st.session_state.jobs_data
    else:
        data = importer.DataImport.fetch_and_clean_data(max_rows=1000)
        st.session_state.jobs_data = data
        return data

# ---------- SKILL EXTRACTION FUNCTIONS ----------
def extract_skills(description):
    tech_skills = {
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust",
        "r", "matlab", "scala", "perl", "shell", "bash",
        "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "asp.net",
        "jquery", "bootstrap", "sass", "less", "webpack", "next.js", "nuxt.js",
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle", "sqlite",
        "dynamodb", "neo4j", "firebase", "bigquery", "snowflake",
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible", "circleci", "git",
        "prometheus", "grafana", "elk stack", "splunk", "new relic", "datadog",
        "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "data analysis", "statistics", "spss", "tableau", "power bi", "looker", "d3.js", "matplotlib",
        "seaborn", "jupyter", "hHeightsadoop", "spark", "kafka", "airflow", "dbt",
        "react native", "flutter", "ios", "android", "xcode", "android studio",
        "security", "penetration testing", "ethical hacking", "firewall", "vpn", "ssl", "encryption",
        "agile", "scrum", "jira", "confluence", "trello", "asana", "project management",
        "rest api", "graphql", "microservices", "ci/cd", "blockchain", "web3", "solidity",
        "unity", "unreal engine", "game development", "ar", "vr", "iot", "edge computing",
        "communication", "leadership", "problem solving", "teamwork", "office"
    }
    if not description:
        return []
    desc = description.lower()
    found = []
    for skill in tech_skills:
        if skill in desc:
            if skill == 'r' and not any(x in desc for x in ['ruby', 'rust', 'react']):
                found.append(skill)
            elif skill != 'r':
                found.append(skill)
    return sorted(found)

def extract_skills_data(jobs_data):
    if jobs_data is None or jobs_data.empty:
        return pd.DataFrame()
    all_skills = []
    
    # Check if 'description' column exists, otherwise use 'description_tokens'
    if 'description' in jobs_data.columns:
        # Original approach - extract skills from description text
        for desc in jobs_data['description'].dropna():
            if isinstance(desc, str):
                skills = extract_skills(desc)
                all_skills.extend(skills)
    elif 'description_tokens' in jobs_data.columns:
        # Alternative approach - use already tokenized skills
        for tokens in jobs_data['description_tokens'].dropna():
            if isinstance(tokens, list):
                all_skills.extend(tokens)
            elif isinstance(tokens, str):
                # Handle case where tokens might be a string representation of a list
                skills = tokens.strip("[]").replace("'", "").split(", ")
                all_skills.extend([s.strip() for s in skills if s.strip()])
    
    counts = Counter(all_skills)
    total = len(jobs_data)
    data = []
    for skill, count in counts.items():
        if count >= 5:
            popularity = (count / total) * 100
            growth = np.random.uniform(0, 15)  # Dummy "Recent Growth (%)"
            category = "Unknown"
            if any(x in str(skill).lower() for x in ["python", "r", "java", "c++", "javascript"]):
                category = "Programming"
            elif any(x in str(skill).lower() for x in ["sql", "database", "postgresql"]):
                category = "Data"
            elif any(x in str(skill).lower() for x in ["aws", "azure", "gcp", "cloud"]):
                category = "Cloud"
            elif any(x in str(skill).lower() for x in ["ml", "ai", "machine learning", "tensorflow", "pytorch"]):
                category = "AI"
            elif any(x in str(skill).lower() for x in ["react", "angular", "vue", "html", "css"]):
                category = "Web Development"
            elif any(x in str(skill).lower() for x in ["docker", "kubernetes", "devops", "ci/cd"]):
                category = "DevOps"
            elif any(x in str(skill).lower() for x in ["excel", "word", "powerpoint", "office"]):
                category = "Office"
            elif any(x in str(skill).lower() for x in ["tableau", "power bi", "looker", "visualization"]):
                category = "Visualization"
            data.append({
                "Skill": skill,
                "Popularity (%)": popularity,
                "Recent Growth (%)": growth,
                "Category": category
            })
    return pd.DataFrame(data)

# ---------- GEMINI INSIGHT FUNCTION ----------
def get_gemini_insight(skills_list):
    prompt = (
        "You are an experienced career advisor with expertise in technology skills. "
        "Provide a concise, plain-language key insight regarding the importance, trends, and career benefits "
        "of the following skills: " + ", ".join(skills_list) + ". "
        "Break your response into clear sections with bullet points, using simple language."
    )
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating insight: {e}")
        return "Unable to generate insight at this time."

# ---------- MAIN APPLICATION ----------
def main():
    st.markdown('<p style="font-size: 2.5rem; font-weight: bold; color: #6eb52f;">Top Skills for Tech Professionals</p>', unsafe_allow_html=True)
    
    # Refresh Data Button
    if st.button("🔄 Refresh Data", key="refresh_data"):
        jobs_data = importer.DataImport.fetch_and_clean_data(max_rows=1000)
        st.session_state.jobs_data = jobs_data
        if jobs_data is not None and not jobs_data.empty:
            st.success("Job data reloaded!")
        else:
            st.error("Failed to load job data.")
    
    # Load Jobs Data
    jobs_data = load_jobs_data()
    if jobs_data is None or jobs_data.empty:
        st.markdown('<div class="empty-state"><h3>No Jobs Data Available</h3><p>Click Refresh Data to load job data.</p></div>', unsafe_allow_html=True)
        return
    
    # -------- Filters Section --------
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">Filters</p>', unsafe_allow_html=True)
    colA = st.columns(1)[0]
    with colA:
        # Removing the Select Countries filter
        selected_countries = []
    st.markdown('</div>', unsafe_allow_html=True)
    # -------- End Filters Section --------
    
    # Extract skills data from filtered jobs data
    df = extract_skills_data(jobs_data)
    if df.empty:
        st.markdown('<div class="empty-state"><h3>No Skills Data Available</h3><p>Could not extract skills. Refresh and try again.</p></div>', unsafe_allow_html=True)
        return
    
    # Get all unique skills
    all_skills = df["Skill"].unique().tolist()
    
    # Skills Filter
    selected_skills = st.multiselect("Filter by Skills", options=all_skills, default=[])
    if selected_skills:
        df = df[df["Skill"].isin(selected_skills)]
    
    # -------- Overall Visualizations Section --------
    st.markdown("### Overall Top Skills")
    chart_data = df.sort_values(by="Popularity (%)", ascending=False).head(10)
    
    viz_option = st.radio("Select Visualization Type", options=["Vertical Bar Chart", "Donut Chart"], horizontal=True)
    if viz_option == "Vertical Bar Chart":
        vbar = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Skill:N", title="Skill", sort="-y"),
            y=alt.Y("Popularity (%):Q", title="Popularity (%)"),
            color=alt.Color("Category:N", legend=alt.Legend(title="Category")),
            tooltip=["Skill", "Popularity (%)", "Recent Growth (%)", "Category"]
        ).properties(width=700, height=400)
        st.altair_chart(vbar, use_container_width=True)
    else:
        fig = px.pie(chart_data, values="Popularity (%)", names="Skill", color="Category",
                     hole=0.4, title="Top Skills Donut Chart")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # -------- Key Insight Section --------
    st.markdown("### Key Insight")
    
    # Select skills directly for insights (instead of selecting by category)
    selected_insight_skills = st.multiselect("Select Skills for Insight", options=all_skills, default=all_skills[:5] if len(all_skills) >= 5 else all_skills)
    
    if selected_insight_skills:
        if st.button("Generate AI Insight for Selected Skills"):
            with st.spinner("Generating AI insight..."):
                ai_insight = get_gemini_insight(selected_insight_skills)
            st.markdown("#### AI-Generated Insight:")
            st.markdown(ai_insight)
    else:
        st.warning("Please select at least one skill for insight.")
    
if __name__ == "__main__":
    main()
