import requests
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import plotly.graph_objects as go


st.set_page_config(
    page_title="CFO & Builder",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page."""
    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Home", "AI Analyst", "SaaS Metrics", "Market Data"],
            icons=["house", "robot", "calculator", "graph-up-arrow"],
            menu_icon="cast",
            default_index=0,
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


def render_market_data() -> None:
    """Display the Market Intelligence dashboard with stock data."""
    st.title("Market Intelligence")
    
    symbol = st.text_input("Ticker Symbol", value="MSFT")
    
    if symbol:
        try:
            with st.spinner(f"Fetching data for {symbol}..."):
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="6mo")
                
                if hist.empty:
                    st.error(f"No data found for ticker symbol: {symbol}")
                    return
                
                # Create candlestick chart
                fig = go.Figure(
                    data=[
                        go.Candlestick(
                            x=hist.index,
                            open=hist["Open"],
                            high=hist["High"],
                            low=hist["Low"],
                            close=hist["Close"],
                        )
                    ]
                )
                
                fig.update_layout(
                    title=f"{symbol} - 6 Month Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    height=600,
                    xaxis_rangeslider_visible=False,
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            st.info("Please check that the ticker symbol is valid and try again.")


def main() -> None:
    """Entrypoint for the Streamlit app."""
    selected = render_sidebar()
    if selected == "Home":
        render_home()
    elif selected == "AI Analyst":
        render_ai_analyst()
    elif selected == "SaaS Metrics":
        st.title("SaaS Efficiency Estimator")
        st.write(
            "Calculate the **Rule of 40** and valuation impact based on standard SaaS metrics."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            arr_growth = st.number_input(
                "ARR Growth (%)", min_value=-100.0, value=25.0, step=1.0
            )
        with col2:
            fcf_margin = st.number_input(
                "FCF Margin (%)", min_value=-100.0, value=10.0, step=1.0
            )
        with col3:
            arr_total = st.number_input("Total ARR ($M)", value=10.0)

        st.divider()

        rule_of_40 = arr_growth + fcf_margin

        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                label="Rule of 40 Score", value=f"{rule_of_40}%", delta=rule_of_40 - 40
            )

        with c2:
            if rule_of_40 >= 40:
                st.success(
                    "✅ **Elite Efficiency**: This company is balancing growth and profitability well."
                )
            elif rule_of_40 >= 20:
                st.warning(
                    "⚠️ **Moderate**: Good growth, but consider improving margins or acceleration."
                )
            else:
                st.error(
                    "❌ **Needs Focus**: Growth plus margin is too low relative to burn."
                )

        st.caption(
            "Strategic Context: Investors typically reward companies above the 40% line with higher revenue multiples."
        )
    elif selected == "Market Data":
        render_market_data()


if __name__ == "__main__":
    main()

