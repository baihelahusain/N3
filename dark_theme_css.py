# Dark theme CSS - remove any background color overrides
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
    
    /* Empty state styles */
    .empty-state {
        text-align: center;
        padding: 40px;
        background-color: #262730;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    /* Compact layout styles */
    .compact-chart {
        margin-top: -10px;
        margin-bottom: -20px;
    }
    
    .compact-header {
        margin-top: -5px;
    }
</style>
""", unsafe_allow_html=True) 