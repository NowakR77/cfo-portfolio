import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


st.set_page_config(
    page_title="Market Data | CFO & Builder",
    page_icon="📈",
    layout="wide",
)

st.title("Market Intelligence")
st.caption("Interactive stock analysis with real-time market data and candlestick charts.")

st.divider()

# Input Section
col1, col2 = st.columns([2, 1])
with col1:
    symbol = st.text_input(
        "Ticker Symbol",
        value="MSFT",
        placeholder="e.g., AAPL, GOOGL, TSLA",
        help="Enter a stock ticker symbol",
    )
with col2:
    period = st.selectbox(
        "Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2,
        help="Select the historical period for the chart",
    )

st.divider()

# Fetch and Display Data
if symbol:
    try:
        with st.spinner(f"Fetching market data for {symbol.upper()}..."):
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                st.error(f"No data found for ticker symbol: {symbol.upper()}")
                st.info("Please verify the ticker symbol and try again.")
            else:
                # Display Key Metrics
                info = ticker.info
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    current_price = hist["Close"].iloc[-1]
                    st.metric(
                        label="Current Price",
                        value=f"${current_price:.2f}",
                        delta=f"${current_price - hist['Close'].iloc[-2]:.2f}" if len(hist) > 1 else None,
                    )

                with col2:
                    st.metric(
                        label="52 Week High",
                        value=f"${hist['High'].tail(252).max():.2f}" if len(hist) >= 252 else "N/A",
                    )

                with col3:
                    st.metric(
                        label="52 Week Low",
                        value=f"${hist['Low'].tail(252).min():.2f}" if len(hist) >= 252 else "N/A",
                    )

                with col4:
                    avg_volume = hist["Volume"].tail(30).mean()
                    st.metric(
                        label="Avg Volume (30d)",
                        value=f"{avg_volume:,.0f}",
                    )

                st.divider()

                # Create Candlestick Chart
                fig = go.Figure(
                    data=[
                        go.Candlestick(
                            x=hist.index,
                            open=hist["Open"],
                            high=hist["High"],
                            low=hist["Low"],
                            close=hist["Close"],
                            name=symbol.upper(),
                        )
                    ]
                )

                fig.update_layout(
                    title=f"{symbol.upper()} - Stock Price Chart ({period})",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    height=600,
                    xaxis_rangeslider_visible=False,
                    template="plotly_white",
                    hovermode="x unified",
                )

                fig.update_xaxes(
                    rangeslider_visible=False,
                    rangeselector=dict(
                        buttons=list(
                            [
                                dict(count=7, label="1W", step="day", stepmode="backward"),
                                dict(count=30, label="1M", step="day", stepmode="backward"),
                                dict(count=90, label="3M", step="day", stepmode="backward"),
                                dict(step="all", label="All"),
                            ]
                        )
                    ),
                )

                st.plotly_chart(fig, use_container_width=True)

                # Additional Information
                with st.expander("📊 View Detailed Statistics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Period High", f"${hist['High'].max():.2f}")
                        st.metric("Period Low", f"${hist['Low'].min():.2f}")
                    with col2:
                        price_change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100
                        st.metric("Period Return", f"{price_change:.2f}%")
                        volatility = (hist["Close"].pct_change().std() * (252 ** 0.5)) * 100
                        st.metric("Annualized Volatility", f"{volatility:.2f}%")

    except Exception as e:
        st.error(f"Error fetching data for {symbol.upper()}: {str(e)}")
        st.info("Please check that the ticker symbol is valid and try again.")

else:
    st.info("👆 Enter a ticker symbol above to view market data and charts.")

