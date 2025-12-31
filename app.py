import streamlit as st
import google.generativeai as genai

# --- ၁။ Page Config & CSS ---
st.set_page_config(page_title="AI Myanmar Script Writer", layout="wide")
st.markdown("""<style>[data-testid="stHeader"], .stAppDeployButton, [data-testid="stStatusWidget"], footer, #MainMenu {visibility: hidden; display:none !important;} .main .block-container { padding-top: 2rem; }</style>""", unsafe_allow_html=True)

# --- ၂။ API Setup ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Billing error ကင်းဝေးစေရန် flash version ကို အသေ သတ်မှတ်ခြင်း
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Setup Error: {e}")
        st.stop()
else:
    st.error("Secrets ထဲမှာ GEMINI_API_KEY ကို မတွေ့ပါ။")
    st.stop()

# --- ၃။ UI ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")
with st.sidebar:
    st.title("🎬 Settings")
    genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance"])
    length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

# --- ၄။ Logic ---
if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
    if topic:
        with st.spinner('AI က စဉ်းစားနေပါတယ်...'):
            try:
                # Billing ရှိတဲ့ key တွေမှာ prompt ကို ပိုတိကျအောင် ပေးရပါမယ်
                response = model.generate_content(f"Write a {genre} movie script about {topic} in Myanmar language. Format: Professional screenplay. Length: {length}.")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Generation Error: {e}")
                st.info("အကြံပြုချက် - Billing ချိတ်ဆက်ထားလျှင် Google Cloud Console တွင် API ကို Enable လုပ်ထားရပါမည်။")
