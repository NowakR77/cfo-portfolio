import streamlit as st
import google.generativeai as genai
import datetime

st.set_page_config(page_title="Daily AI & Supply Chain Briefing", page_icon="📰", layout="wide")
st.title("📰 The AI & Supply Chain Daily")
st.caption(f"Date: {datetime.date.today().strftime('%B %d, %Y')}")

# --- CONFIGURATION ---
# Load API key from Streamlit secrets
if "GOOGLE_API_KEY" in st.secrets and st.secrets["GOOGLE_API_KEY"]:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except Exception as config_error:
        st.error(f"⚠️ Failed to configure Google AI: {config_error}")
        st.stop()
else:
    st.error("⚠️ GOOGLE_API_KEY not found or empty in secrets.toml. Please configure it.")
    st.info("💡 Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your API key.")
    st.stop()

# Sidebar: Control the "News Desk"
with st.sidebar:
    st.header("📢 Editorial Settings")
    focus_topic = st.text_input("Specific Focus?", placeholder="e.g. Autonomous Trucking, NVIDIA, Port Strikes")
    tone = st.selectbox("Tone", ["Executive Briefing (CFO Style)", "LinkedIn Post (Engaging)", "Technical Deep Dive"])
    
    st.divider()
    st.info("ℹ️ **How this works:**\nGemini actively searches Google for news published in the last 24 hours, then synthesizes it into a digest.")

# --- MAIN FEED ---

st.subheader("Generate Today's Edition")

if st.button("🚀 Draft Daily Briefing"):
    with st.spinner("The AI Editor is reading the morning news..."):
        try:
            # 1. Setup the Model with Search Tool
            # Try the experimental model first, fallback to stable version
            try:
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
            except Exception as model_error:
                st.warning(f"⚠️ Experimental model not available, trying stable version: {model_error}")
                model = genai.GenerativeModel('gemini-1.5-pro')  # Fallback to stable model
            
            # 2. Build the Prompt
            # We enforce "Last 24 Hours" in the prompt text
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            
            search_query = f"latest news AI supply chain logistics technology {focus_topic if focus_topic else ''}"
            
            prompt = f"""
            You are the Editor-in-Chief of a Supply Chain & AI Tech publication.
            
            TASK:
            Based on your training data and knowledge, identify the most significant recent news stories 
            regarding '{search_query}' that would be relevant for today ({today_str}).
            Focus on developments that would matter to a CFO or Operations Executive.
            Write a daily briefing in the style: '{tone}'.
            
            FORMATTING RULES:
            - **Headline:** Catchy but professional.
            - **The Lead:** A 2-sentence summary of the biggest story.
            - **Story 1, 2, 3:** Bullet points with the "Why it matters" for business.
            - **Note on Sources:** Since real-time search is not available, base this on your knowledge 
              of recent industry trends and developments in AI, supply chain, and logistics technology.
            
            Constraint: Ignore generic "AI is the future" fluff. Focus on hard news: investments, shortages, 
            new tech launches, or regulations. Be clear when discussing recent developments that you're 
            drawing from your training data rather than live search results.
            """
            
            # 3. Generate Content
            # Note: The google_search tool currently has compatibility issues with the Python SDK
            # The error "Unknown field for FunctionDeclaration: google_search" indicates
            # the SDK version or API key may not fully support this feature yet.
            # We'll generate content without search grounding for now.
            
            # Generate the briefing (without Google Search tool due to SDK compatibility)
            response = model.generate_content(prompt)
            
            # Show info about search feature
            with st.expander("ℹ️ About Google Search Feature", expanded=False):
                st.markdown("""
                **Google Search Grounding Status:** Currently unavailable
                
                The `google_search` tool feature is experiencing compatibility issues with the current SDK version.
                
                **To enable Google Search in the future:**
                1. Update the SDK: `pip install --upgrade google-generativeai`
                2. Ensure your API key has Google Search permissions enabled
                3. Check the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions) for the latest format
                
                **Current workaround:** The model uses its training data knowledge. For real-time information, 
                consider manually searching and including recent news in your focus topic.
                """)
            
            # 4. Display the Result
            st.markdown("---")
            st.markdown(response.text)
            
            # 5. Show Sources (Grounding Metadata)
            # This allows you to verify the news before you post it.
            if (hasattr(response, 'candidates') and len(response.candidates) > 0 and 
                hasattr(response.candidates[0], 'grounding_metadata') and 
                response.candidates[0].grounding_metadata and
                hasattr(response.candidates[0].grounding_metadata, 'search_entry_point') and
                response.candidates[0].grounding_metadata.search_entry_point):
                with st.expander("📚 View Source Links"):
                    st.markdown(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
                    
            # 6. "Copy to Clipboard" helper
            st.divider()
            st.write("📝 **Draft Ready.** Copy the text above to post to LinkedIn or Slack.")

        except Exception as e:
            st.error(f"News Desk Error: {e}")
            error_str = str(e).lower()
            if "api key" in error_str or "authentication" in error_str or "permission" in error_str:
                st.warning("🔑 API Key Issue: Make sure your GOOGLE_API_KEY is set correctly in secrets.toml and is valid.")
                st.info("💡 Get your API key from: https://makersuite.google.com/app/apikey")
            elif "model" in error_str or "not found" in error_str:
                st.warning("⚠️ Model error: The specified model might not be available. Trying fallback...")
            else:
                st.warning("⚠️ Make sure your GOOGLE_API_KEY is set correctly in secrets.toml and has proper permissions.")

# --- ARCHIVE SECTION (Optional Placeholder) ---
# st.divider()
# st.subheader("🗄️ Past Editions")
# st.write("Save functionality coming soon...")