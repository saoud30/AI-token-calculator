import streamlit as st
import tiktoken
import json
from streamlit_echarts import st_echarts

def count_tokens(text, model="gpt-3.5-turbo"):
    encoder = tiktoken.encoding_for_model(model)
    return len(encoder.encode(text))

def tokenize_text(text, model="gpt-3.5-turbo"):
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    return [encoder.decode([token]) for token in tokens]

# Set page config with dark theme
st.set_page_config(page_title="Token Calculator", page_icon="🧮", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark mode
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #3b82f6;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
    }
    .stTextArea textarea {
        background-color: #1e293b;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #4b5563;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1e293b;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #4b5563;
    }
    .token-box {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1r6slb0 {
        gap: 2rem 3rem;
    }
    .stAlert {
        background-color: #2d3748;
        color: #ffffff;
    }
    .st-emotion-cache-16idsys p {
        color: #a0aec0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧮 Token Calculator")
st.markdown("Calculate and visualize token consumption for different GPT models.")

col1, col2 = st.columns([2, 1])

with col1:
    text = st.text_area("Enter your text here:", height=200)

with col2:
    model = st.selectbox(
        "Select GPT Model",
        ["gpt-4", "gpt-3.5-turbo", "gpt-3", "text-davinci-002"]
    )
    
    if text:
        tokens = count_tokens(text, model)
        characters = len(text)
        
        st.markdown("### 📊 Token Statistics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Tokens", tokens, delta=None, delta_color="off")
        with col_b:
            st.metric("Characters", characters, delta=None, delta_color="off")
        
        # Token to character ratio visualization
        option = {
            "backgroundColor": 'rgba(0,0,0,0)',
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "name": "Token Stats",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#0e1117",
                        "borderWidth": 2,
                    },
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "label": {"show": True, "fontSize": "20", "fontWeight": "bold", "color": "#ffffff"}
                    },
                    "labelLine": {"show": False},
                    "data": [
                        {"value": tokens, "name": "Tokens", "itemStyle": {"color": "#3b82f6"}},
                        {"value": characters - tokens, "name": "Characters (non-token)", "itemStyle": {"color": "#60a5fa"}},
                    ],
                }
            ],
        }
        st_echarts(options=option, height="200px")

if text:
    st.markdown("### 🔤 Tokenized Text")
    tokenized = tokenize_text(text, model)
    
    html = '<div class="token-box">'
    for i, token in enumerate(tokenized):
        color = f"hsl({(i * 137) % 360}, 70%, 50%)"
        html += f'<span style="background-color: {color}; padding: 0 3px; border-radius: 3px; margin: 0 1px; display: inline-block; color: #000000;">{token}</span>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("### 📋 Token Details")
    token_details = [{"index": i, "token": token} for i, token in enumerate(tokenized)]
    st.json(json.dumps(token_details, ensure_ascii=False, indent=2))

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; font-size: 0.9rem;">
    <p>This tool uses the <code>tiktoken</code> library to tokenize text similarly to OpenAI's models.</p>
    <p>Note: The exact tokenization may vary slightly from OpenAI's implementation.</p>
</div>
""", unsafe_allow_html=True)