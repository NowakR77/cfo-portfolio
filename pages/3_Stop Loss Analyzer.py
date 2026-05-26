import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Bloomberg AI Analyzer", page_icon="🛡️", layout="wide")
st.title("🛡️ AI Stop-Loss Strategist (Bloomberg Edition)")

# 1. Sidebar Inputs
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Stock Ticker", value="", placeholder="e.g. NVDA, TSLA").upper()
    period = st.selectbox("Lookback Period", ["3mo", "6mo", "1y"], index=1)
    risk_tolerance = st.select_slider("Risk Tolerance", options=["Conservative", "Moderate", "Aggressive"], value="Moderate")
    
    st.divider()
    st.caption("ℹ️ **New Metrics:**")
    st.caption("* **RSI:** <30 is Oversold (Buy signal?), >70 is Overbought.")
    st.caption("* **Volume:** High volume confirms the trend.")

# 2. Main Logic
if ticker:
    with st.spinner(f"Fetching market data for {ticker}..."):
        try:
            # Download data
            df = yf.download(ticker, period=period)

            # --- FLATTEN FIX (Essential for yfinance) ---
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
            # --------------------------------------------

            if df.empty:
                st.warning(f"Could not find data for '{ticker}'.")
                st.stop()

            # 3. The Math Engine (Now with RSI & Volume)
            # Calculate ATR (Volatility) — Wilder's smoothing, same as pandas_ta
            high, low, close = df['High'], df['Low'], df['Close']
            prev_close = close.shift(1)
            tr = pd.concat([
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs()
            ], axis=1).max(axis=1)
            df['ATRr_14'] = tr.ewm(com=13, adjust=False, min_periods=14).mean()

            # Calculate RSI (Momentum) — Wilder's smoothing, same as pandas_ta
            delta = close.diff()
            gain = delta.clip(lower=0)
            loss = (-delta).clip(lower=0)
            avg_gain = gain.ewm(com=13, adjust=False, min_periods=14).mean()
            avg_loss = loss.ewm(com=13, adjust=False, min_periods=14).mean()
            rs = avg_gain / avg_loss
            df['RSI_14'] = 100 - (100 / (1 + rs))

            # Calculate Volume SMA (Average Volume over 20 days)
            vol_sma = df['Volume'].rolling(window=20).mean()
            
            # Get latest values
            current_price = float(df['Close'].iloc[-1])
            current_atr = float(df['ATRr_14'].iloc[-1])
            current_rsi = float(df['RSI_14'].iloc[-1])
            current_vol = float(df['Volume'].iloc[-1])
            avg_vol = float(vol_sma.iloc[-1])

            # Analyze Volume Status
            vol_ratio = current_vol / avg_vol
            if vol_ratio > 1.2:
                vol_status = "High (Institutions Active)"
            elif vol_ratio < 0.8:
                vol_status = "Low (Weak Conviction)"
            else:
                vol_status = "Normal"

            # Calculate Stop Loss
            multiplier = 3.0 if risk_tolerance == "Conservative" else 2.0 if risk_tolerance == "Moderate" else 1.5
            stop_price = current_price - (current_atr * multiplier)
            stop_pct = ((current_price - stop_price) / current_price) * 100

            # 4. Dashboard Display (2 Rows of Metrics)
            st.subheader("📊 Market Condition")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${current_price:.2f}")
            col2.metric("Suggested Stop Loss", f"${stop_price:.2f}", f"-{stop_pct:.1f}%")
            col3.metric("RSI (Momentum)", f"{current_rsi:.1f}", "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral")
            col4.metric("Volume Trend", vol_status, f"{vol_ratio:.1f}x Avg")

            # 5. Visual Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index,
                            open=df['Open'], high=df['High'],
                            low=df['Low'], close=df['Close'],
                            name='Price'))
            fig.add_hline(y=stop_price, line_dash="dash", line_color="red", annotation_text="Stop Loss")
            fig.update_layout(title=f"{ticker} Price Action", height=500, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # 6. AI Analysis Button
            st.divider()
            st.subheader("🤖 Bloomberg AI Analyst")
            
            if st.button(f"Analyze {ticker} with Advanced Metrics"):
                with st.spinner("Consulting AI Risk Manager..."):
                    try:
                        # --- VERIFY YOUR URL HERE ---
                        api_url = "https://robertnowak30.app.n8n.cloud/webhook/stock-risk"
                        # ----------------------------

                        payload = {
                            "ticker": ticker,
                            "price": f"{current_price:.2f}",
                            "stop_loss": f"{stop_price:.2f}",
                            "volatility": f"{current_atr:.2f}",
                            "rsi": f"{current_rsi:.1f}",
                            "volume_status": vol_status,
                            "risk_profile": risk_tolerance
                        }

                        response = requests.post(api_url, json=payload, timeout=60)
                        
                        if response.status_code == 200:
                            # Use the robust JSON parsing we built earlier
                            data = response.json()
                            analysis = data.get("content", data.get("output", data.get("text", "")))
                            
                            st.success("Analysis Complete")
                            with st.chat_message("assistant"):
                                st.markdown(analysis)
                        else:
                            st.error(f"Server Error {response.status_code}")
                            
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")

        except Exception as e:
            st.error(f"Data Error: {e}")