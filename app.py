import streamlit as st
import google.generativeai as genai

# ၁။ သင့်ရဲ့ API Key ကို ဒီမှာ သေချာထည့်ပါ
API_KEY = "AIzaSyBRiv9KJyq3cKU70QxrNeVZ_8jQVL7FNqU"

st.set_page_config(page_title="AI Myanmar Script Writer", page_icon="🎬", layout="wide")

try:
    genai.configure(api_key=API_KEY)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    model = genai.GenerativeModel(model_name)

    # --- SIDEBAR စတင်ခြင်း ---
    with st.sidebar:
        st.title("⚙️ Settings")
        st.subheader("ဇာတ်လမ်းပုံစံ ရွေးချယ်ပါ")
        
        # ဇာတ်လမ်းအမျိုးအစား ရွေးရန်
        genre = st.selectbox(
            "Genre (အမျိုးအစား):",
            ["Drama (အလွမ်း/ဒရာမာ)", "Action (အက်ရှင်)", "Horror (သရဲ/ထိတ်လန့်ချောက်ချား)", "Comedy (ဟာသ)", "Romance (အချစ်)"]
        )
        
        # ဇာတ်လမ်းအရှည် ရွေးရန် (Optional)
        length = st.radio("ဇာတ်လမ်းအရှည်:", ["တိုတိုနှင့်လိုရင်း", "အသေးစိတ် ဇာတ်ညွှန်း"])
        
        st.divider()
        st.info("အမျိုးအစား ရွေးပြီးရင် ညာဘက်မှာ အကြောင်းအရာ ရိုက်ထည့်ပါ။")

    # --- MAIN PAGE စတင်ခြင်း ---
    st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")
    
    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ ရေးပါ:", placeholder="ဥပမာ - နယ်မြို့လေးတစ်မြို့မှာ ဖြစ်ပျက်တဲ့ ထူးဆန်းတဲ့ လူသတ်မှုတစ်ခုအကြောင်း")

    if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
        if topic:
            with st.spinner(f'{genre} ဇာတ်လမ်းကို မြန်မာလို ရေးနေပါပြီ...'):
                # Prompt ထဲမှာ Sidebar က ရွေးထားတဲ့ Genre ကို ထည့်သွင်းခြင်း
                prompt = f"""
                Act as a native Myanmar professional screenwriter. 
                Write a {genre} movie script about: {topic}
                Script Length: {length}

                Rules:
                1. Language: Use natural, conversational Myanmar Language (Burmese). 
                2. Avoid: Do not use formal/bookish Burmese in dialogues.
                3. Tone: The tone must match the {genre} style (e.g., if Horror, make it scary; if Comedy, make it funny).
                4. Dialogues: Use realistic daily spoken Burmese like 'ပဲ', 'တယ်', 'မှာလား', 'ဟာ'. 
                5. Format: Professional screenplay with Scene Headings, Action, and Character Names.
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader(f"✨ {genre} ဇာတ်ညွှန်း ရလဒ်")
                st.markdown(response.text)
        else:
            st.warning("အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ")

except Exception as e:
    st.error(f"Error: {e}")
