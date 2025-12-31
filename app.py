import streamlit as st
import google.generativeai as genai

# ၁။ သင့်ရဲ့ API Key ကို ဒီမှာ ထည့်ပါ
API_KEY = "AIzaSyBRiv9KJyq3cKU70QxrNeVZ_8jQVL7FNqU"

st.set_page_config(page_title="AI Myanmar Script Writer", page_icon="🎬", layout="wide")

# --- CSS: Toolbar များကိုသာ သီးသန့်ရွေးဖျောက်ခြင်း ---
hide_all_style = """
            <style>
            /* အပေါ်က ဘားတန်းတစ်ခုလုံးကို ဖျောက်ခြင်း */
            [data-testid="stHeader"] {display:none !important;}
            
            /* ခဲတံပုံ (Deploy Button) ကို ဖျောက်ခြင်း */
            .stAppDeployButton {display:none !important;}
            
            /* GitHub Icon နှင့် Status Widget ကို ဖျောက်ခြင်း */
            [data-testid="stStatusWidget"] {display:none !important;}
            
            /* Footer ကို ဖျောက်ခြင်း */
            footer {display: none !important;}
            
            /* စာသားတွေ အပေါ်ကပ်မနေအောင် နေရာချခြင်း */
            .main .block-container {
                padding-top: 3rem;
            }
            </style>
            """
st.markdown(hide_all_style, unsafe_allow_html=True)

# --- Title ကို ပုံမှန် Header စာသားအဖြစ် ပြန်ရေးခြင်း ---
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")
st.write("လူရေးသလို သဘာဝကျတဲ့ မြန်မာဇာတ်ညွှန်းများ ဖန်တီးပေးပါသည်")

try:
    genai.configure(api_key=API_KEY)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    model = genai.GenerativeModel(model_name)

    # --- Sidebar ---
    with st.sidebar:
        st.title("🎬 Settings")
        genre = st.selectbox(
            "ဇာတ်လမ်းအမျိုးအစား:",
            ["Drama", "Action", "Horror", "Comedy", "Romance", "Thriller"]
        )
        length = st.radio("ဇာတ်လမ်းအရှည်:", ["တိုတိုနှင့်လိုရင်း", "အသေးစိတ် ဇာတ်ညွှန်း"])

    # --- Main Page Content ---
    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဥပမာ - ရန်ကုန်မြို့က စုံထောက်တစ်ယောက်အကြောင်း")

    if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
        if topic:
            with st.spinner('ခဏစောင့်ပါ...'):
                prompt = f"Act as a native Myanmar screenwriter. Write a {genre} script about {topic}. Use natural Burmese spoken language."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("အကြောင်းအရာ ရိုက်ထည့်ပါ")

except Exception as e:
    st.error(f"Error: {e}")
