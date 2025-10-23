import streamlit as st
import requests
import json

# Configuration
# API_URL = "http://127.0.0.1:8000"
API_URL = "https://smart-content-generator-lhue.onrender.com/"

# Page configuration
st.set_page_config(
    page_title="Smart Content Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 1rem;
    }
    .big-font {
        font-size: 1.2rem !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Smart Content Generator")
st.markdown("**Powered by Google Gemini AI** | FastAPI Backend")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Status Check
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get("gemini_api") == "configured":
                st.success("✅ API Connected")
            else:
                st.warning("⚠️ API running but Gemini key not configured")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Not Running")
        st.info("Make sure to run: `uvicorn main:app --reload`")
    
    st.markdown("---")
    st.markdown("### 📚 Features")
    st.markdown("""
    - ✨ Text Generation
    - 📝 Summarization
    - 🌐 Translation
    - 💻 Code Explanation
    - ❓ Q&A System
    """)
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Saim Shakeel**")
    st.markdown("[GitHub](https://github.com/saim963) | [Email](mailto:aims3328@gmail.com)")
    
    st.markdown("---")
    st.markdown("### 📊 Tech Stack")
    st.markdown("""
    - FastAPI
    - Google Gemini AI
    - Streamlit
    - Python
    """)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✨ Generate Text", 
    "📝 Summarize", 
    "🌐 Translate", 
    "💻 Explain Code", 
    "❓ Q&A"
])

# Tab 1: Generate Text
with tab1:
    st.header("✨ Generate Text")
    st.markdown("Generate creative content using AI")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_area(
            "Enter your prompt:",
            placeholder="e.g., Write a short story about a robot learning to paint...",
            height=150,
            key="generate_prompt"
        )
    
    with col2:
        st.markdown("### Controls")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative"
        )
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=2000,
            value=500,
            step=100
        )
    
    if st.button("🚀 Generate", type="primary", use_container_width=True):
        if not prompt:
            st.error("⚠️ Please enter a prompt!")
        else:
            with st.spinner("✨ Generating content..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/generate",
                        json={
                            "prompt": prompt, 
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("✅ Generated successfully!")
                        st.markdown("### 📄 Result:")
                        st.markdown(f"```\n{data['data']['generated_text']}\n```")
                        
                        # Copy button
                        st.download_button(
                            label="📥 Download Result",
                            data=data['data']['generated_text'],
                            file_name="generated_text.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")
                    st.info("Make sure the API is running on http://127.0.0.1:8000")

# Tab 2: Summarize
with tab2:
    st.header("📝 Summarize Text")
    st.markdown("Condense long articles into concise summaries")
    
    text_to_summarize = st.text_area(
        "Enter text to summarize:",
        placeholder="Paste your long article or text here...",
        height=200,
        key="summarize_text"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.selectbox(
            "Summary Length:",
            options=["short", "medium", "long"],
            index=1,
            format_func=lambda x: {
                "short": "📝 Short (2-3 sentences)",
                "medium": "📄 Medium (1 paragraph)",
                "long": "📃 Long (2-3 paragraphs)"
            }[x]
        )
    
    with col2:
        char_count = len(text_to_summarize) if text_to_summarize else 0
        st.metric("Character Count", char_count)
    
    if st.button("📝 Summarize", type="primary", use_container_width=True):
        if not text_to_summarize:
            st.error("⚠️ Please enter text to summarize!")
        elif char_count < 50:
            st.warning("⚠️ Text is too short. Please enter at least 50 characters.")
        else:
            with st.spinner("📝 Summarizing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/summarize",
                        json={"text": text_to_summarize, "length": length}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("✅ Summarized successfully!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Length", f"{data['data']['original_length']} chars")
                        with col2:
                            st.metric("Summary Length", f"{data['data']['summary_length']} chars")
                        
                        st.markdown("### 📄 Summary:")
                        st.info(data["data"]["summary"])
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Summary",
                            data=data['data']['summary'],
                            file_name="summary.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")

# Tab 3: Translate
with tab3:
    st.header("🌐 Translate Text")
    st.markdown("Translate text to multiple languages")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_to_translate = st.text_area(
            "Enter text to translate:",
            placeholder="Hello, how are you today?",
            height=150,
            key="translate_text"
        )
    
    with col2:
        target_language = st.selectbox(
            "Target Language:",
            options=["Spanish", "French", "German", "Hindi", "Chinese", 
                    "Japanese", "Arabic", "Russian", "Italian", "Portuguese"]
        )
        
        # Language emoji mapping
        language_emoji = {
            "Spanish": "🇪🇸", "French": "🇫🇷", "German": "🇩🇪",
            "Hindi": "🇮🇳", "Chinese": "🇨🇳", "Japanese": "🇯🇵",
            "Arabic": "🇸🇦", "Russian": "🇷🇺", "Italian": "🇮🇹",
            "Portuguese": "🇵🇹"
        }
        
        st.markdown(f"### {language_emoji.get(target_language, '🌐')} {target_language}")
    
    if st.button("🌐 Translate", type="primary", use_container_width=True):
        if not text_to_translate:
            st.error("⚠️ Please enter text to translate!")
        else:
            with st.spinner(f"🌐 Translating to {target_language}..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/translate",
                        json={"text": text_to_translate, "target_language": target_language}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("✅ Translated successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 🔤 Original")
                            st.info(data['data']['original'])
                        
                        with col2:
                            st.markdown(f"### {language_emoji.get(target_language, '🌐')} {target_language}")
                            st.success(data['data']['translated'])
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Translation",
                            data=data['data']['translated'],
                            file_name=f"translation_{target_language.lower()}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")

# Tab 4: Explain Code
with tab4:
    st.header("💻 Explain Code")
    st.markdown("Get detailed explanations of code snippets")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        language = st.selectbox(
            "Programming Language:",
            options=["Python", "JavaScript", "Java", "C++", "C#", "PHP", 
                    "Ruby", "Go", "Rust", "Swift"]
        )
        
        # Language icon mapping
        language_icon = {
            "Python": "🐍", "JavaScript": "📜", "Java": "☕",
            "C++": "⚙️", "C#": "💠", "PHP": "🐘",
            "Ruby": "💎", "Go": "🔷", "Rust": "🦀", "Swift": "🍎"
        }
        
        st.markdown(f"### {language_icon.get(language, '💻')} {language}")
    
    with col1:
        code_snippet = st.text_area(
            "Enter your code:",
            placeholder="def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
            height=200,
            key="code_snippet"
        )
    
    if st.button("💻 Explain Code", type="primary", use_container_width=True):
        if not code_snippet:
            st.error("⚠️ Please enter code to explain!")
        else:
            with st.spinner("💻 Analyzing code..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/explain-code",
                        json={"code": code_snippet, "language": language}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("✅ Code explained successfully!")
                        
                        st.markdown("### 📖 Explanation:")
                        st.markdown(data['data']['explanation'])
                        
                        # Show original code in expander
                        with st.expander("📝 View Original Code"):
                            st.code(data['data']['code'], language=language.lower())
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Explanation",
                            data=data['data']['explanation'],
                            file_name="code_explanation.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")

# Tab 5: Q&A
with tab5:
    st.header("❓ Question & Answer")
    st.markdown("Ask any question and get detailed answers")
    
    question = st.text_area(
        "Your Question:",
        placeholder="What is machine learning?",
        height=100,
        key="qa_question"
    )
    
    context = st.text_input(
        "Context (Optional):",
        placeholder="e.g., In the context of modern AI applications",
        key="qa_context"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("❓ Get Answer", type="primary", use_container_width=True):
            if not question:
                st.error("⚠️ Please enter a question!")
            else:
                with st.spinner("🤔 Thinking..."):
                    try:
                        payload = {"question": question}
                        if context:
                            payload["context"] = context
                        
                        response = requests.post(
                            f"{API_URL}/api/qa",
                            json=payload
                        )
                        data = response.json()
                        
                        if data.get("success"):
                            st.success("✅ Answer generated!")
                            
                            # Display question
                            st.markdown("### ❓ Question:")
                            st.info(data['data']['question'])
                            
                            # Display context if provided
                            if data['data'].get('context_provided'):
                                st.markdown("### 📝 Context:")
                                st.caption(context)
                            
                            # Display answer
                            st.markdown("### 💡 Answer:")
                            st.success(data['data']['answer'])
                            
                            # Download button
                            download_content = f"Question: {data['data']['question']}\n\n"
                            if context:
                                download_content += f"Context: {context}\n\n"
                            download_content += f"Answer: {data['data']['answer']}"
                            
                            st.download_button(
                                label="📥 Download Q&A",
                                data=download_content,
                                file_name="qa_result.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ Connection Error: {str(e)}")
    
    # Sample questions
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    
    sample_questions = [
        "What is the difference between supervised and unsupervised learning?",
        "Explain how neural networks work in simple terms",
        "What are the benefits of using FastAPI over Flask?",
        "How does async/await work in Python?"
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, sample in enumerate(sample_questions):
        with col1 if idx % 2 == 0 else col2:
            if st.button(f"📌 {sample[:40]}...", key=f"sample_{idx}"):
                st.session_state.qa_question = sample
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p>Built with ❤️ by Saim Shakeel | Powered by FastAPI + Google Gemini AI + Streamlit</p>
    <p>
        <a href="https://github.com/saim963" target="_blank">GitHub</a> | 
        <a href="mailto:aims3328@gmail.com">Email</a>
    </p>
</div>
""", unsafe_allow_html=True)