import streamlit as st
import google.generativeai as genai

# ၁။ သင့်ရဲ့ API Key ကို ဒီမှာ အစားထည့်ပါ
API_KEY = "AIzaSyBRiv9KJyq3cKU70QxrNeVZ_8jQVL7FNqU"

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Myanmar Script Writer", 
    page_icon="🎬", 
    layout="wide"
)

# --- CSS: Toolbar, Header, Footer များ အပြီးအပိုင်ဖျောက်ရန် ---
hide_st_style = """
            <style>
            [data-testid="stStatusWidget"] {display:none;}
.st-emotion-cache-1kyx60p {display:none;} /* GitHub icon class */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stHeader"] {display:none;}
            [data-testid="stToolbar"] {display:none;}
            /* Background အရောင်ကို အနည်းငယ် ပြောင်းလဲပေးခြင်း (Optional) */
            .stApp {
                background-color: #f8f9fa;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- AI Model Setup ---
try:
    genai.configure(api_key=API_KEY)
    # ရနိုင်တဲ့ model ကို ရှာခြင်း
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    model = genai.GenerativeModel(model_name)

    # --- Sidebar Setup ---
    with st.sidebar:
        st.title("🎬 Script Settings")
        st.markdown("---")
        genre = st.selectbox(
            "ဇာတ်လမ်းအမျိုးအစား ရွေးပါ:",
            ["Drama (ဒရာမာ)", "Action (အက်ရှင်)", "Horror (သရဲ)", "Comedy (ဟာသ)", "Romance (အချစ်)", "Thriller (သည်းထိတ်ရင်ဖို)"]
        )
        length = st.radio("ဇာတ်လမ်းအရှည်:", ["တိုတိုနှင့်လိုရင်း", "အသေးစိတ် ဇာတ်ညွှန်း"])
        st.divider()
        st.caption("Developed by AI Writer Pro")

    # --- Main Interface ---
    st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")
    st.write("သင့်ရဲ့ ဇာတ်လမ်းအကြမ်းဖျင်းကို ရိုက်ထည့်လိုက်ပါ။ AI က လူရေးသလို သဘာဝကျကျ ရေးပေးပါလိမ့်မယ်။")

    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ:", height=150, placeholder="ဥပမာ - ရန်ကုန်မြို့ညတစ်ညမှာ ဖြစ်ပျက်တဲ့ ထူးဆန်းတဲ့ အဖြစ်အပျက်တစ်ခု...")

    if st.button("ဇာတ်ညွှန်းကို ယခုဖန်တီးမယ်"):
        if topic:
            with st.spinner(f'{genre} ပုံစံဖြင့် မြန်မာလို ရေးသားနေပါသည်...'):
                # Human-Style Prompt Engineering
                prompt = f"""
                Act as a native Myanmar professional screenwriter. 
                Write a {genre} movie script about: {topic}
                Script Length: {length}

                Rules:
                1. Language: Use natural, conversational Myanmar Language (Burmese). 
                2. Avoid: Do not use formal/bookish Burmese like 'သည်', '၏' in dialogues.
                3. Dialogues: Use realistic daily spoken Burmese as humans do. 
                4. Emotions: Add deep human emotions and realistic character reactions.
                5. Format: Professional screenplay format with Scene Headings and Character Names.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader(f"✨ {genre} Script Result")
                st.markdown(response.text)
                
                # Download Button (Optional)
                st.download_button(
                    label="ဇာတ်ညွှန်းကို သိမ်းဆည်းရန် (Download)",
                    data=response.text,
                    file_name="myanmar_script.txt",
                    mime="text/plain"
                )
        else:
            st.warning("ကျေးဇူးပြု၍ ဇာတ်လမ်းအကြောင်းအရာ အရင်ရိုက်ထည့်ပါ။")

except Exception as e:
    st.error(f"Error: {e}")
    st.info("API Key မှန်မမှန် သို့မဟုတ် အင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပေးပါ။")

