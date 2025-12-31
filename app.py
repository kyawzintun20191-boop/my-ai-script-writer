import streamlit as st
import google.generativeai as genai

# ၁။ သင့်ရဲ့ API Key ကို ဒီမှာ သေချာထည့်ပါ
API_KEY = "AIzaSyBRiv9KJyq3cKU70QxrNeVZ_8jQVL7FNqU"

st.set_page_config(page_title="AI Myanmar Script Writer", page_icon="🎬")
st.title("🎭 AI မြန်မာဇာတ်ညွှန်းရေးဆရာ")

try:
    genai.configure(api_key=API_KEY)
    
    # ရနိုင်တဲ့ model တွေကို အလိုအလျောက် ရှာခိုင်းခြင်း
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    st.caption(f"Connected with: {model_name}")
    model = genai.GenerativeModel(model_name)

    topic = st.text_area("ဇာတ်လမ်းအကြောင်းအရာ ရေးပါ:", "ဥပမာ - ရန်ကုန်မြို့က စုံထောက်တစ်ယောက်အကြောင်း")

    if st.button("ဇာတ်ညွှန်းထုတ်ရန်"):
        if topic:
            with st.spinner('မြန်မာလို ရေးနေပါပြီ... ခဏစောင့်ပါ...'):
                # ဒီနေရာမှာ Tab/Space အကွာအဝေး မှန်ဖို့ အရေးကြီးပါတယ်
                prompt = f"""
                Act as a native Myanmar professional screenwriter. 
                Write a movie script about: {topic}

                Rules:
                1. Language: Use natural, conversational Myanmar Language (Burmese). 
                2. Avoid: Do not use "formal/bookish" Burmese like 'သည်', '၏' in dialogues.
                3. Dialogues: Use realistic daily spoken Burmese like 'ပဲ', 'တယ်', 'မှာလား', 'ဟာ'. 
                4. Emotions: Add deep human emotions and realistic character reactions.
                5. Format: Professional screenplay with Scene Headings, Action, and Character Names.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("အကြောင်းအရာ တစ်ခုခု အရင်ရိုက်ထည့်ပါ")

except Exception as e:
    st.error(f"Error: {e}")
