import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from streamlit_lottie import st_lottie

# ---------- CONFIGURATIONS ----------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
    
    /* Chat styling */
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .user-message {
        background-color: #3a3c4f;
        color: white;
        margin-left: 20px;
    }
    
    .ai-message {
        background-color: #262730;
        color: white;
        margin-right: 20px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

#------------Side bar animation------------------------------------------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# All sidebar content is defined inside this block.
with st.sidebar:
    # Navigation widget for your top pages

    # Animation section: mountain-themed animation for "on top"
    st.markdown("### Gemini Advisor: Your Smart Guide to Career Success!")
    # Replace the URL below with any mountain top or summit-themed Lottie animation.
    lottie_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_3vbOcw.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="mountain_anim")
    else:
        st.error("Animation could not be loaded.")
#-------------------End here-----------------------------------------------


import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ---------- CONFIGURATIONS ----------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# System prompt defining strict career-related guidelines
system_prompt = (
    "You are an AI career advisor specializing in technology career guidance. Your name is Gemini Advisor.\n\n"
    "Guidelines:\n"
    "1. ONLY answer questions related to job skills, education, career development, and tech industry trends.\n"
    "2. Keep responses focused on factual information about job market trends, relevant skills, educational paths, and career development.\n"
    "3. If asked about anything unrelated to careers, skills, education, or tech industry trends, respond with: \"I'm focused on helping with career and skill development questions. Please ask something related to job skills, education, or tech industry trends.\"\n"
    "4. Provide clear, practical, and actionable advice based on current industry knowledge.\n"
    "5. Do not make up information or statistics - acknowledge if you don't have specific data.\n"
    "6. Format responses with sections and bullet points for readability.\n\n"
    "NEVER discuss topics unrelated to professional development, career guidance, tech skills, or education trends."
)

def get_gemini_response(user_question):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    # Combine the system prompt with the user's question
    prompt = system_prompt + "\nUser Question: " + user_question
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        st.error(f"🤖 AI Error: {e}")
        return None

def main():
    st.markdown('<p style="font-size: 3.0rem; font-weight: bold; color: #6eb52f;">Gemini Advisor - Career Q&A</p>', unsafe_allow_html=True)

    
    st.markdown("""
    <div class="info-box">
        <p>Ask Gemini Advisor questions about job skills, career development, education paths, and tech industry trends. 
        Gemini Advisor will provide insights strictly based on the guidelines below:</p>
        <ul>
            <li>Answer only career-related questions.</li>
            <li>Provide clear, actionable, and fact-based advice.</li>
            <li>If the question is off-topic, remind the user to ask about career and skill development.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Suggested Questions")
    suggested_questions = [
        "What skills should I learn for a career in data science?",
        "What's the best path to become a software engineer?",
        "Which programming languages are most in demand?",
        "What certifications are valuable for tech careers?",
        "How can I transition into a tech career?"
    ]
    for question in suggested_questions:
        if st.button(question, key=f"suggested_{question}"):
            st.session_state.user_input = question

    user_question = st.text_input("Enter your question:", key="user_input")
    
    if st.button("Ask Question"):
        if user_question:
            with st.spinner("Engaging neural networks..."):
                response = get_gemini_response(user_question)
            if response:
                st.subheader("Gemini Advisor Response:")
                st.markdown(response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()




