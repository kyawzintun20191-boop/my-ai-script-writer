import streamlit as st
import google.generativeai as genai

# API Key ကို Secrets ကနေ ယူပါ (Settings > Secrets ထဲမှာ GEMINI_API_KEY ဆိုပြီး ထည့်ထားပေးရပါမယ်)
try:
    API_KEY = st.secrets["AIzaSyBRiv9KJyq3cKU70QxrNeVZ_8jQVL7FNqU"]
except:
    st.error("Secrets ထဲမှာ API Key ထည့်ဖို့ မေ့နေပါတယ်!")
    st.stop()

st.set_page_config(page_title="AI Myanmar Script Writer", page_icon="🎬", layout="wide")

# CSS: Toolbar တွေကိုပဲ သီးသန့်ဖျောက်ပြီး Title ကို ချန်ထားမယ်
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

# Title ကို ပုံမှန် စာသားအဖြစ် ရေးသားခြင်း
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    with st.sidebar:
        st.title("🎬 Settings")
        genre = st.selectbox("အမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy"])
        length = st.radio("အရှည်:", ["တိုတို", "အရှည်"])

    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")

    if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
        if topic:
            with st.spinner('AI က ဇာတ်လမ်း စဉ်းစားနေပါတယ်...'):
                prompt = f"Write a {genre} movie script about {topic} in natural Myanmar spoken language."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("အကြောင်းအရာ ရိုက်ထည့်ပါ")

except Exception as e:
    st.error(f"Error: {e}")
