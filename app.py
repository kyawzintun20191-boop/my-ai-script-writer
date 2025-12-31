import streamlit as st
import google.generativeai as genai

# --- ၁။ Page Configuration ---
st.set_page_config(page_title="AI Myanmar Script Writer", layout="wide")

# --- ၂။ CSS: Toolbar များကို ဖျောက်ခြင်း ---
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

# --- ၃။ Initialize Model ---
# Secrets ထဲက Key ကို ယူပြီး model ကို အရင်ဆောက်ထားပါမယ်
try:
    if "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါ။")
        st.stop()
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- ၄။ UI Components ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

with st.sidebar:
    st.title("🎬 Settings")
    genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance"])
    length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

# --- ၅။ Generation Logic ---
if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
    if topic:
        with st.spinner('AI က ရေးပေးနေပါတယ်...'):
            try:
                # model ကို ဒီနေရာကနေ သေချာပေါက် ခေါ်သုံးလို့ရပါပြီ
                prompt = f"Write a {genre} movie script about {topic} in natural Myanmar spoken language. Length: {length}."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("✨ ထွက်ပေါ်လာသော ဇာတ်ညွှန်း")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Generation Error: {e}")
    else:
        st.warning("အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ။")
