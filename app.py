import streamlit as st
import google.generativeai as genai

# --- ၁။ Secrets ထဲက Key ကို နာမည်တူအောင် ယူခြင်း ---
try:
    # ပုံ (1wd.png) ထဲကအတိုင်း GEMINI_API_KEY ဆိုတဲ့ နာမည်ကို သုံးထားပါတယ်
    key = st.secrets["AIzaSyBykUrcbqFzaSu_bMJEaS8KyPW7nLPpwks"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Secrets Error: {e}")
    st.info("Streamlit Dashboard > Settings > Secrets ထဲမှာ GEMINI_API_KEY ရှိမရှိ ပြန်စစ်ပေးပါ")
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
