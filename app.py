import streamlit as st
import google.generativeai as genai

# Secrets ထဲက နာမည်နဲ့ အတိအကျ တူရပါမယ်
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error: API Key ကို Secrets ထဲမှာ ရှာမတွေ့ပါ။ {e}")
    st.stop()

# --- ၂။ Page Configuration & UI Cleaning ---
st.set_page_config(page_title="AI Myanmar Script Writer", layout="wide")

st.markdown("""
    <style>
    [data-testid="stHeader"] {display:none !important;}
    .stAppDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    footer {display: none !important;}
    #MainMenu {visibility: hidden;}
    .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- ၃။ Main UI ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

with st.sidebar:
    st.title("🎬 Settings")
    genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance"])
    length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
    if topic:
        with st.spinner('AI က ရေးပေးနေပါတယ်...'):
            try:
                prompt = f"Write a {genre} movie script about {topic} in natural Myanmar spoken language. Length: {length}."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Generation Error: {e}")
    else:
        st.warning("အကြောင်းအရာ ရိုက်ထည့်ပါ")
