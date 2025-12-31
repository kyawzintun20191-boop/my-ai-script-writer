import streamlit as st
import google.generativeai as genai

# --- ၁။ Page Configuration ---
st.set_page_config(page_title="AI Myanmar Script Writer", layout="wide")

# --- ၂။ CSS: Toolbar ဖျောက်ခြင်း ---
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

# --- ၃။ Initialize API & Model ---
# ပုံ (1wd.png) ထဲကအတိုင်း GEMINI_API_KEY နာမည်ကို သုံးထားပါတယ်
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 404 Error မတက်အောင် model နာမည်ကို 'gemini-1.5-flash-latest' လို့ ပြောင်းသုံးကြည့်ပါမယ်
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"Model Initialization Error: {e}")
        st.stop()
else:
    st.error("Secrets ထဲမှာ GEMINI_API_KEY ကို မတွေ့ပါ။")
    st.stop()

# --- ၄။ UI Design ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

with st.sidebar:
    st.title("🎬 Settings")
    genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance"])
    length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

# --- ၅။ Generation Logic ---
if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
    if topic:
        with st.spinner('AI က ဇာတ်လမ်း ရေးသားနေပါသည်...'):
            try:
                full_prompt = f"Write a {genre} movie script about {topic} in natural Myanmar spoken language. Use professional screenplay format. Length: {length}."
                
                # Content ထုတ်လုပ်ခြင်း
                response = model.generate_content(full_prompt)
                
                if response.text:
                    st.markdown("---")
                    st.subheader(f"✨ {genre} Result")
                    st.markdown(response.text)
                else:
                    st.error("AI က အဖြေမထုတ်ပေးနိုင်ပါ။ အကြောင်းအရာကို ပြန်ပြင်ရိုက်ကြည့်ပါ။")
            except Exception as e:
                # Error message အသေးစိတ်ကို ပြပေးရန်
                st.error(f"Generation Error: {e}")
                st.info("API Key သက်တမ်းကုန်နေတာမျိုး သို့မဟုတ် Model Name လွဲနေတာမျိုး ဖြစ်နိုင်ပါတယ်။")
    else:
        st.warning("အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ။")
