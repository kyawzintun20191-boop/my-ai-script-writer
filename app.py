import streamlit as st
import google.generativeai as genai

# --- ၁။ Page Config & CSS (Toolbar ဖျောက်ခြင်း) ---
st.set_page_config(page_title="AI Myanmar Script Writer", layout="wide")
st.markdown("""
    <style>
    [data-testid="stHeader"], .stAppDeployButton, [data-testid="stStatusWidget"], footer, #MainMenu {
        visibility: hidden; display:none !important;
    }
    .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- ၂။ API & Model Setup ---
# Secrets ထဲက GEMINI_API_KEY ကို နာမည်တူအောင် ယူသုံးပါမယ်
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Model နာမည်ကို ရိုးရိုးရှင်းရှင်း gemini-1.5-flash လို့ပဲ သုံးပါမယ်
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Secrets ထဲမှာ GEMINI_API_KEY ကို မတွေ့ပါ။")
    st.stop()

# --- ၃။ User Interface ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

with st.sidebar:
    st.title("🎬 Settings")
    genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance"])
    length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

# --- ၄။ Script Generation ---
if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
    if topic:
        with st.spinner('AI က ဇာတ်လမ်း ရေးသားနေပါသည်...'):
            try:
                # Prompt ကို ပိုမိုတိကျစေရန် ပြင်ဆင်ထားပါသည်
                prompt = f"Write a {genre} movie script about {topic} in natural Myanmar spoken language. Use professional screenplay format. Length: {length}."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("---")
                    st.subheader(f"✨ {genre} Result")
                    st.markdown(response.text)
            except Exception as e:
                # Billing Error တက်နေပါက ဒီနေရာမှာ ပြပေးပါမယ်
                st.error(f"Generation Error: {e}")
                st.info("အကယ်၍ Billing error တက်နေပါက API Key အသစ် (Project အသစ်တွင်) ထုတ်ယူရန် လိုအပ်ပါသည်။")
    else:
        st.warning("အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ။")
