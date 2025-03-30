# Custom CSS for dark theme
st.markdown("""
<style>
    /* Title Styles */
    .page-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #6eb52f !important;
        margin-bottom: 1rem !important;
    }
    
    .section-header {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .filter-container {
        background: #262730;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .insight-card {
        background-color: #31343a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #6eb52f !important;
    }
    
    .metric-label {
        font-size: 1rem !important;
    }
    
    /* Compact layout styles */
    .compact-chart {
        margin-top: -10px;
        margin-bottom: -20px;
    }
    
    .compact-header {
        margin-top: -5px;
    }
    
    /* Empty state styles */
    .empty-state {
        text-align: center;
        padding: 40px;
        background-color: #262730;
        border-radius: 12px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True) 