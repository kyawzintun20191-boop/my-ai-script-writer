import streamlit as st
import google.generativeai as genai

# --- ၁။ Secrets ထဲက API Key ကို ယူခြင်း ---
try:
    # Streamlit Cloud ရဲ့ Settings > Secrets ထဲမှာ GEMINI_API_KEY ဆိုပြီး ထည့်ထားရပါမယ်
    API_KEY = st.secrets["AIzaSyBykUrcbqFzaSu_bMJEaS8KyPW7nLPpwks"]
except Exception:
    st.error("Error: API Key ကို Secrets ထဲမှာ ရှာမတွေ့ပါ။ ကျေးဇူးပြု၍ Settings > Secrets ထဲမှာ GEMINI_API_KEY ကို ထည့်ပေးပါ။")
    st.stop()

# --- ၂။ Page Configuration ---
st.set_page_config(page_title="AI Myanmar Script Writer", page_icon="🎬", layout="wide")

# --- ၃။ CSS: Toolbar များကို ဖျောက်ပြီး Title ကို ချန်ထားခြင်း ---
st.markdown("""
    <style>
    /* အပေါ်က Header ဘားတန်းကို ဖျောက်ခြင်း */
    [data-testid="stHeader"] {display:none !important;}
    
    /* ခဲတံပုံ (Deploy Button) ကို ဖျောက်ခြင်း */
    .stAppDeployButton {display:none !important;}
    
    /* GitHub Icon နှင့် Status Widget ကို ဖျောက်ခြင်း */
    [data-testid="stStatusWidget"] {display:none !important;}
    
    /* Footer (Made with Streamlit) ကို ဖျောက်ခြင်း */
    footer {display: none !important;}
    
    /* Main Menu ကို ဖျောက်ခြင်း */
    #MainMenu {visibility: hidden;}
    
    /* အပေါ်ဆုံးက Title အရမ်းကပ်မနေအောင် နေရာချခြင်း */
    .main .block-container { padding-top: 2rem; }
    
    /* Sidebar ကို ပိုသေသပ်အောင်လုပ်ခြင်း */
    [data-testid="stSidebar"] {
        background-color: #f1f3f6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ၄။ AI Model Setup ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- ၅။ Sidebar (Settings) ---
    with st.sidebar:
        st.title("🎬 Script Settings")
        genre = st.selectbox("ဇာတ်လမ်းအမျိုးအစား:", ["Drama", "Action", "Horror", "Comedy", "Romance", "Thriller"])
        length = st.radio("ဇာတ်လမ်းအရှည်:", ["တိုတိုနှင့်လိုရင်း", "အသေးစိတ် ဇာတ်ညွှန်း"])
        st.divider()
        st.caption("Developed by AI Writer Pro")

    # --- ၆။ Main Interface ---
    st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")
    st.write("လူရေးသလို သဘာဝကျတဲ့ မြန်မာဇာတ်ညွှန်းများ ဖန်တီးပေးပါသည်")

    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဥပမာ - ရန်ကုန်မြို့ညတစ်ညမှာ ဖြစ်ပျက်တဲ့ ထူးဆန်းတဲ့ အဖြစ်အပျက်တစ်ခု...")

    if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
        if topic:
            with st.spinner(f'{genre} ပုံစံဖြင့် ရေးသားနေပါသည်...'):
                prompt = f"""
                Act as a native Myanmar professional screenwriter. 
                Write a {genre} movie script about: {topic}
                Script Length: {length}

                Rules:
                1. Language: Use natural, conversational Myanmar Language (Burmese). 
                2. Avoid: Do not use formal/bookish Burmese (သည်/၏) in dialogues.
                3. Format: Professional screenplay format with Scene Headings and Action.
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader(f"✨ {genre} Result")
                st.markdown(response.text)
        else:
            st.warning("ကျေးဇူးပြု၍ အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ။")

except Exception as e:
    st.error(f"တစ်ခုခုမှားယွင်းနေပါသည်: {e}")
