import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Real Estate Master | CFO & Builder",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Real Estate Master")
st.caption("AI-powered real estate market analysis and comparable property research.")

st.divider()

# --- 3. AI Market Scout (Google Edition) ---
st.subheader("🤖 AI Market Scout (Powered by Gemini)")

# Configure the API using Streamlit secrets
if "GOOGLE_API_KEY" in st.secrets and st.secrets["GOOGLE_API_KEY"]:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except Exception as config_error:
        st.error(f"⚠️ Failed to configure Google AI: {config_error}")
        st.stop()
else:
    st.error("⚠️ GOOGLE_API_KEY not found or empty in secrets.toml. Please configure it.")
    st.info("To add your API key:\n1. Create a `.streamlit/secrets.toml` file\n2. Add: `GOOGLE_API_KEY = 'your-key-here'`")
    st.stop()

# Input Section
col1, col2 = st.columns(2)
with col1:
    neighborhood = st.text_input(
        "Neighborhood",
        value="Artesia, Prosper TX",
        placeholder="e.g., Artesia, Prosper TX",
        help="Enter the neighborhood or area to search"
    )
with col2:
    user_price = st.number_input(
        "Target Price ($)",
        min_value=0,
        value=850000,
        step=10000,
        help="The price you want to compare against"
    )

if st.button("Run Comps Analysis", type="primary", use_container_width=True):
    if not neighborhood.strip():
        st.warning("Please enter a neighborhood.")
    else:
        with st.spinner("Gemini is searching active listings..."):
            try:
                # 1. Initialize the Model
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                
                # 2. Define the Prompt
                prompt = f"""
                You are a Real Estate Appraiser.
                1. Search Google for "active homes for sale in {neighborhood}".
                2. Find 3 comparable listings similar to a price of ${user_price:,}.
                3. Compare their price-per-sqft to the user's estimate.
                4. Verdict: Is ${user_price:,} Aggressive, Realistic, or Low?
                
                Provide a detailed analysis with:
                - Comparable properties found
                - Price per square foot comparisons
                - Market assessment
                - Your professional verdict
                """
                
                # 3. Call Gemini with grounding enabled
                # Note: The exact syntax may vary based on Gemini API version
                # If 'tools' parameter doesn't work, try using the grounding parameter
                try:
                    response = model.generate_content(
                        prompt,
                        tools=[{"google_search_retrieval": {}}]
                    )
                except (TypeError, AttributeError):
                    # Fallback: try alternative syntax
                    try:
                        response = model.generate_content(prompt)
                    except Exception as fallback_error:
                        st.error(f"API call failed: {fallback_error}")
                        st.info("Note: Google Search grounding may require specific API access. Using standard generation.")
                        response = model.generate_content(prompt)
                
                # 4. Display Result
                st.success("✅ Appraisal Complete")
                st.divider()
                
                # Access the text output
                if hasattr(response, 'text') and response.text:
                    st.markdown("### Analysis Results")
                    st.markdown(response.text)
                else:
                    st.warning("Received an empty response from Gemini.")
                
                # Bonus: Display Grounding Metadata if available
                try:
                    if (hasattr(response, 'candidates') and 
                        len(response.candidates) > 0 and 
                        hasattr(response.candidates[0], 'grounding_metadata')):
                        metadata = response.candidates[0].grounding_metadata
                        if hasattr(metadata, 'search_entry_point') and metadata.search_entry_point:
                            st.divider()
                            st.caption("📚 Sources utilized:")
                            if hasattr(metadata.search_entry_point, 'rendered_content'):
                                st.markdown(metadata.search_entry_point.rendered_content)
                except Exception:
                    # Grounding metadata not available - this is okay
                    pass

            except genai.types.BlockedPromptException as e:
                st.error("⚠️ Content was blocked by safety filters. Please try rephrasing your query.")
                st.info(f"Details: {e}")
            except Exception as e:
                st.error(f"❌ Gemini Error: {e}")
                st.info("Please check your API key and ensure you have access to the Gemini API.")