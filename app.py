import requests
import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="CFO & Builder",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown("### Navigation")
        selected = option_menu(
            menu_title="",
            options=["Home", "AI Analyst"],
            icons=["house", "robot"],
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "#0d6efd", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "padding": "10px"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            },
        )
    return selected


def render_home() -> None:
    """Display the home page content."""
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "profile.jpg",
            width=200,
        )

    with col2:
        st.title("Robert Nowak")
        st.subheader("CFO & Builder | Finance x AI")
        st.write(
            """
            **Bridging the gap between traditional Finance leadership and modern AI automation.**

            I am a Finance Executive based in Prosper, Texas, focused on building scalable financial operations.
            Unlike traditional CFOs, I believe in "walking the walk"—building my own tools, automating workflows,
            and leveraging AI to drive business insights.
            """
        )
        st.markdown(
            "[Connect on LinkedIn](https://www.linkedin.com) | [Email Me](mailto:your-email@example.com)"
        )

    st.divider()

    st.subheader("🚀 What I Build")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("**AI Agents**\nAutomated research and analysis tools using LLMs.")
    with c2:
        st.success("**SaaS Metrics**\nDashboards for ARR, NRR, and Rule of 40.")
    with c3:
        st.warning("**Workflows**\nProcess automation using n8n and Python.")

    st.write("---")
    st.caption("📍 Currently building in Python, Streamlit, and n8n.")


def render_ai_analyst() -> None:
    """Display the AI analyst page and handle memo generation."""
    st.title("Institutional Research Agent")
    st.caption("Automated memos for fast diligence.")

    company = st.text_input("Company or Ticker", placeholder="e.g., NVDA")
    generate = st.button("Generate Memo", type="primary")

    if generate:
        if not company.strip():
            st.warning("Please enter a company name or ticker.")
            return

        with st.spinner("Drafting memo..."):
            try:
                response = requests.post(
                    "https://robertnowak30.app.n8n.cloud/webhook/research-agent",
                    json={"query": company.strip()},
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                content = payload.get("content", "").strip()

                if not content:
                    st.error("The research agent returned an empty response.")
                    return

                st.markdown(content)
            except requests.RequestException as exc:
                st.error(f"Unable to reach the research agent: {exc}")
            except ValueError:
                st.error("Received an unexpected response from the research agent.")


def main() -> None:
    """Entrypoint for the Streamlit app."""
    page = render_sidebar()
    if page == "Home":
        render_home()
    elif page == "AI Analyst":
        render_ai_analyst()


if __name__ == "__main__":
    main()

