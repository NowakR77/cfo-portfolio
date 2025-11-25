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
    st.title("CFO & Builder")
    st.caption("Finance leader shaping data-driven operating systems.")

    st.markdown(
        """
        <style>
            .about-card {
                background-color: #f9fafc;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
            }
            .photo-placeholder {
                width: 200px;
                height: 240px;
                border-radius: 16px;
                border: 2px dashed #94a3b8;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                color: #475569;
                background: #fff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_photo, col_about = st.columns([1, 2])

    with col_photo:
        st.markdown(
            """
            <div class="photo-placeholder">
                Photo Placeholder
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_about:
        st.markdown(
            """
            <div class="about-card">
                <h3>About Me</h3>
                <p>
                    I architect finance organizations that operate like product teams—tight
                    feedback loops, intelligent automation, and relentless focus on strategic
                    allocation. With experience across corporate finance, SaaS GTM analytics,
                    and venture-backed scale-ups, I pair CFO rigor with a builder's mindset to
                    design resilient systems that unlock growth.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


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

