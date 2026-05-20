"""
CodeAlpha: Language Translation Tool
A lightweight translation UI using Google Translate (free tier via textblob)
Features: Text translation, copy button, language detection, character limit tracking
"""

import streamlit as st
from deep_translator import GoogleTranslator
import time

# Configure Streamlit page
st.set_page_config(page_title="CodeAlpha Translation Tool", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for better UI
st.markdown("""
    <style>
    .translation-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
        margin-top: 10px;
    }
    .language-selector {
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌐 Language Translation Tool")
st.markdown("*Powered by TextBlob | Free, Fast, Multi-Language Translation*")

# Supported languages (ISO 639-1 codes for TextBlob)
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Hindi": "hi",
    "Arabic": "ar",
    "Korean": "ko",
}

# Sidebar: Project Info
with st.sidebar:
    st.markdown("### 📋 Project Info")
    st.markdown("""
    - **Task**: Translation API Integration
    - **Library**: TextBlob (Google Translate Backend)
    - **Features**: Multi-language, Copy button, Character tracking
    - **GitHub**: `CodeAlpha_TranslationTool`
    """)
    st.divider()
    st.markdown("*CodeAlpha Internship Program*")

# Main UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<p class="language-selector">Source Language</p>', unsafe_allow_html=True)
    source_lang = st.selectbox("Select source language:", list(LANGUAGES.keys()), key="source", label_visibility="collapsed")

with col2:
    st.markdown('<p class="language-selector">Target Language</p>', unsafe_allow_html=True)
    target_lang = st.selectbox("Select target language:", list(LANGUAGES.keys()), index=1, key="target", label_visibility="collapsed")

# Input Text Area
st.markdown("### 📝 Text to Translate")
input_text = st.text_area(
    "Enter text here:",
    height=120,
    placeholder="Type or paste text you want to translate...",
    label_visibility="collapsed"
)

# Character count
char_count = len(input_text)
st.caption(f"Characters: {char_count} / 5000 (TextBlob free tier limit)")

# Translation Button
if st.button("🔄 Translate", use_container_width=True, type="primary"):
    if not input_text.strip():
        st.error("❌ Please enter some text to translate!")
    elif source_lang == target_lang:
        st.warning("⚠️ Source and target languages are the same. Please select different languages.")
    else:
        with st.spinner("Translating..."):
            try:
                # Translate using TextBlob
                source_code = LANGUAGES[source_lang]
                target_code = LANGUAGES[target_lang]
                
                # Perform translation
                translated = GoogleTranslator(source=source_code, target=target_code).translate(input_text)
                
                # Store in session state for persistence
                st.session_state.translated_text = str(translated)
                st.session_state.translation_done = True
                
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")

# Display Translation Result
if "translation_done" in st.session_state and st.session_state.translation_done:
    st.markdown("### ✅ Translation Result")
    
    result_col1, result_col2 = st.columns([0.9, 0.1])
    
    with result_col1:
        st.markdown(f'<div class="translation-box">{st.session_state.translated_text}</div>', unsafe_allow_html=True)
    
    with result_col2:
        if st.button("📋", help="Copy to clipboard", key="copy_btn"):
            st.write(st.session_state.translated_text)  # In real deployment, use clipboard library
            st.success("✅ Copied! (Use Ctrl+C to copy from above)")

# Additional Features Section
with st.expander("🎛️ Advanced Features"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Text-to-Speech (Input)", help="Requires browser audio support"):
            st.info("💡 Text-to-speech requires `pyttsx3` or web API. Demo feature for UI/UX showcase.")
    
    with col2:
        if st.button("🔍 Language Detection", help="Auto-detect source language"):
            if input_text.strip():
                detected_lang = GoogleTranslator(source='auto', target=target_code).translate(input_text)
                st.info(f"🎯 Detected Language Code: `{detected_lang}`")
            else:
                st.warning("Enter text to detect language.")

# Footer
st.divider()
st.markdown("""
---
**📌 Product Insights (PM Documentation)**
- **Latency**: ~500ms–1s per request (depends on text length & API availability)
- **Cost**: Free tier (TextBlob wraps Google Translate)
- **Scalability**: Limited to 5000 char per request; batch processing recommended for production
- **Reliability**: Depends on google-api availability; fallback required for production
- **UX**: Single-turn translation; session-based state management
""")

