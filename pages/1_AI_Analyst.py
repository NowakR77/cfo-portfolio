import requests
import streamlit as st


st.set_page_config(
    page_title="AI Analyst | CFO & Builder",
    page_icon="🤖",
    layout="wide",
)

st.title("Shares Research Agent")
st.caption("Automated memos for fast diligence and research analysis.")

st.divider()

# Input Section
company = st.text_input(
    "Company or Ticker",
    placeholder="e.g., NVDA, Apple, Microsoft",
    help="Enter a company name or stock ticker symbol",
)

generate = st.button("Generate Memo", type="primary", use_container_width=True)

st.divider()

# Process Request
if generate:
    if not company.strip():
        st.warning("Please enter a company name or ticker symbol.")
    else:
        with st.spinner(f"Analyzing {company.strip()}..."):
            try:
                response = requests.post(
                    "https://robertnowak30.app.n8n.cloud/webhook/research-agent",
                    json={"query": company.strip()},
                    timeout=60,
                )
                response.raise_for_status()
                payload = response.json()
                content = payload.get("content", "").strip()

                if not content:
                    st.error("The research agent returned an empty response.")
                else:
                    st.markdown("### Research Memo")
                    st.markdown(content)
                    
            except requests.RequestException as e:
                st.error(f"Unable to reach the research agent: {e}")
                st.info("Please check your connection and try again.")
            except ValueError:
                st.error("Received an unexpected response format from the research agent.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

