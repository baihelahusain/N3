import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Custom CSS
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
    
    /* About page specific styles */
    .about-section {
        margin-bottom: 30px;
    }
    
    .tech-stack-item {
        display: inline-block;
        margin: 5px;
        padding: 8px 15px;
        background-color: #262730;
        border-radius: 20px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)
#00000---------sidebar-----------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# All sidebar content is defined inside this block.
with st.sidebar:
    # Navigation widget for your top pages

    # Animation section: mountain-themed animation for "on top"
    st.markdown("### Connect with Neural Net Ninjas")
    # Replace the URL below with any mountain top or summit-themed Lottie animation.
    lottie_animation = load_lottie_url("https://lottie.host/e3ebc585-ff11-467d-b7df-06c8159aabe8/2EotAwBySN.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="mountain_anim")
    else:
        st.error("Animation could not be loaded.")

#9------------end here ----------------

def main():
    # Title styled similarly to the main dashboard
    st.markdown('<p style="font-size: 3.0rem; font-weight: bold; color: #6eb52f;">About N3DN.Tech</p>', unsafe_allow_html=True)
    
    # Sub-header with an emoji for extra flair
    st.markdown('<p class="sub-header">Empowering Tech Careers 🚀</p>', unsafe_allow_html=True)
    
    # Credits Section
    st.markdown("## Credits & Acknowledgments")
    st.markdown("""
    This project leverages state-of-the-art tools and APIs to deliver exceptional data-driven insights:
    
    - <span class="emoji">🔍</span> **Serp API**: Providing reliable search data integration.
    - <span class="emoji">🤖</span> **Gemini**: Powering advanced AI features.
    - <span class="emoji">🚀</span> **Streamlit**: Enabling the creation of interactive and user-friendly dashboards.
    """, unsafe_allow_html=True)
    
    # Mission Section
    st.markdown("## Our Mission")
    st.markdown("""
    At **N3DN.Tech**, our goal is to empower technology professionals with comprehensive analytics to make informed career decisions. 
    We bring together job market trends, skill analytics, and salary insights to give you the competitive edge in today's dynamic tech landscape.
    """)
    
    st.markdown("---")
    st.markdown("""
    For more details, visit our [GitHub repository](https://github.com/Shwetanlondhe24/HM0043_Team-Neural-Net-Ninjas) or connect with us on social media.
    """)
    
if __name__ == "__main__":
    main()
