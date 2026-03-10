"""
Main Streamlit Application - AI Blog Generator
A user-friendly web interface for generating articles with AI
"""

import streamlit as st
from content_generator import generate_blog, generate_title, generate_meta_description
from utils import count_words, count_characters, calculate_reading_time, format_reading_time, validate_input
import time

# Page configuration
st.set_page_config(
    page_title="AI Blog/Article Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
    }
    .stats-box {
        background-color: #90d6ff;
        border: 1px solid #b3d9ff;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "generated_article" not in st.session_state:
    st.session_state.generated_article = None
if "article_title" not in st.session_state:
    st.session_state.article_title = None
if "article_meta" not in st.session_state:
    st.session_state.article_meta = None

# Header
st.markdown("<h1 class='main-header'>📝 AI Blog/Article Generator</h1>", unsafe_allow_html=True)
st.markdown("*Powered by OpenAI GPT | Generate high-quality articles in seconds*")
st.markdown("---")

# Sidebar - Settings and Input
with st.sidebar:
    st.header("⚙️ Settings & Configuration")
    
    # Input fields
    topic = st.text_input(
        "✍️ Blog Topic",
        placeholder="e.g., The Future of AI in Finance",
        help="Enter the main topic for your article"
    )
    
    keywords = st.text_input(
        "🏷️ Keywords (comma-separated)",
        placeholder="e.g., machine learning, Risk, Fraud analytics",
        help="Include relevant keywords for SEO and content relevance"
    )
    
    tone = st.selectbox(
        "🎭 Tone/Style",
        ["Professional", "Casual", "Technical"],
        help="Choose the writing style for your article"
    )
    
    length = st.slider(
        "📏 Article Length (words)",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Target word count for the generated article"
    )
    
    st.markdown("---")
    
    # Generate button
    generate_button = st.button(" 🤖 Generate Article", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📚 Example Prompts")
    examples = [
        ("Finance", "machine learning, Risk, Fraud analytics", "Professional", 800),
        ("Remote Work", "flexibility, productivity, challenges", "Casual", 700),
        ("Web3", "blockchain, smart contracts, decentralization", "Technical", 1000),
    ]
    
    for ex_topic, ex_keywords, ex_tone, ex_length in examples:
        if st.button(f"📄 {ex_topic}", use_container_width=True):
            topic = ex_topic
            keywords = ex_keywords
            tone = ex_tone
            length = ex_length
            st.rerun()

# Main content area
if generate_button:
    # Validation
    is_valid, error_msg = validate_input(topic, keywords)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        # Generate content
        with st.spinner("✨ Generating your article... This may take a moment."):
            try:
                # Generate article
                article = generate_blog(topic, keywords, tone, length)
                st.session_state.generated_article = article
                
                # Generate title and meta
                st.session_state.article_title = generate_title(topic, keywords)
                st.session_state.article_meta = generate_meta_description(article)
                
                st.success("✅ Article generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating article: {str(e)}")

# Display generated content
if st.session_state.generated_article:
    # Article Title
    st.markdown("---")
    st.markdown(f"### 📄 {st.session_state.article_title}")
    
    # Meta Description
    with st.expander("📋 SEO Meta Description"):
        st.info(st.session_state.article_meta)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    word_count = count_words(st.session_state.generated_article)
    char_count = count_characters(st.session_state.generated_article)
    reading_time = calculate_reading_time(st.session_state.generated_article)
    formatted_reading_time = format_reading_time(reading_time)
    
    with col1:
        st.metric("📊 Word Count", word_count)
    with col2:
        st.metric("🔡 Character Count", char_count)
    with col3:
        st.metric("⏱️ Reading Time", formatted_reading_time)
    with col4:
        st.metric("🎯 Tone", tone)
    
    st.markdown("---")
    
    # Article Content
    st.markdown("### 📰 Blog/Article Content")
    st.write(st.session_state.generated_article)
    
    st.markdown("---")
    
    # Download Options
    st.subheader("💾 Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download as TXT
        st.download_button(
            label="📥 Download as .txt",
            data=st.session_state.generated_article,
            file_name=f"{st.session_state.article_title.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Download with metadata
        full_content = f"{st.session_state.article_title}\n\nMeta Description: {st.session_state.article_meta}\n\nKeywords: {keywords}\n\n{st.session_state.generated_article}"
        st.download_button(
            label="📥 Download as .txt (with metadata)",
            data=full_content,
            file_name=f"{st.session_state.article_title.replace(' ', '_')}_full.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        # Copy to clipboard button (informational)
        st.info("💡 Use Ctrl+C to copy article from above")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>Made using Streamlit and OpenAI GPT</p>
        <p>© 2026 AI Content Generator </p>
    </div>
""", unsafe_allow_html=True)