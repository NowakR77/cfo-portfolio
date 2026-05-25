import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="AI Investment Scout", page_icon="🚀", layout="wide")
st.title("🚀 AI Investment Opportunity Scout (2026 Edition)")

# 1. Sidebar: Define the Search
with st.sidebar:
    st.header("Target Company")
    ticker = st.text_input("Ticker Symbol", value="", placeholder="e.g. PLTR, SNOW, MSFT").upper()
    
    st.divider()
    st.info("ℹ️ **The 'Rule of 40':**\nA SaaS metric where Growth % + Profit Margin % should be > 40. High scores indicate a healthy 'Winner'.")

if ticker:
    with st.spinner(f"Auditing financials for {ticker}..."):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # --- 2. EXTRACT KEY FINANCIALS ---
            # We use .get() to avoid crashing if data is missing
            current_price = info.get('currentPrice', 0)
            market_cap = info.get('marketCap', 0) / 1e9 # In Billions
            
            # Growth & Margins
            rev_growth = info.get('revenueGrowth', 0) * 100
            profit_margin = info.get('profitMargins', 0) * 100
            
            # Valuation
            pe_ratio = info.get('forwardPE', 0)
            ps_ratio = info.get('priceToSalesTrailing12Months', 0)

            # The "Rule of 40" Calculation
            rule_of_40 = rev_growth + profit_margin
            
            # --- 3. DISPLAY THE SCORECARD ---
            st.subheader(f"📊 Financial Scorecard: {info.get('shortName', ticker)}")
            
            # Row 1: The "Health Check"
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Market Cap", f"${market_cap:.1f}B")
            c2.metric("Revenue Growth (YoY)", f"{rev_growth:.1f}%")
            c3.metric("Profit Margin", f"{profit_margin:.1f}%")
            
            # Rule of 40 Logic (Color coding)
            c4.metric("Rule of 40 Score", f"{rule_of_40:.1f}", delta="✅ Elite" if rule_of_40 > 40 else "⚠️ Needs Work")

            # Row 2: Valuation
            st.caption("Valuation Metrics:")
            v1, v2, v3 = st.columns(3)
            v1.metric("Price/Sales (P/S)", f"{ps_ratio:.2f}x")
            v1.caption("Lower is cheaper")
            
            v2.metric("Forward P/E", f"{pe_ratio:.2f}x")
            v2.caption("Earnings multiple")
            
            target_price = info.get('targetMeanPrice', 0)
            upside = ((target_price - current_price) / current_price) * 100 if target_price else 0
            v3.metric("Analyst Target", f"${target_price:.2f}", f"{upside:.1f}% Upside")

            st.divider()

            # --- 4. THE AI "MOAT CHECK" ---
            st.subheader("🧠 AI Moat Analysis (VC Agent)")
            st.write("Does this company have a defensible advantage, or is it just hype?")
            
            if st.button(f"Launch VC Due Diligence for {ticker}"):
                with st.spinner(f"🕵️‍♂️ Investigating {ticker}'s technology stack and patents..."):
                    try:
                        # --- PASTE YOUR N8N URL HERE ---
                        api_url = "https://robertnowak30.app.n8n.cloud/webhook/ai-moat-check"
                        # -------------------------------
                        
                        # Pack the financial data to help the AI contextualize
                        payload = {
                            "ticker": ticker,
                            "rule_40": f"{rule_of_40:.1f}",
                            "growth": f"{rev_growth:.1f}",
                            "ps_ratio": f"{ps_ratio:.2f}"
                        }
                        
                        response = requests.post(api_url, json=payload, timeout=90) # 90s timeout for deep search
                        
                        if response.status_code == 200:
                            data = response.json()
                            analysis = data.get("content", data.get("output", data.get("text", "")))
                            
                            st.success("Due Diligence Complete")
                            with st.chat_message("assistant", avatar="🕵️‍♂️"):
                                st.markdown(analysis)
                        else:
                            st.error(f"Agent Connection Error: {response.status_code}")
                            
                    except Exception as e:
                        st.error(f"Failed to connect to VC Agent: {e}")

        except Exception as e:
            st.error(f"Could not retrieve financial data. The ticker might be delisted or data unavailable. Error: {e}")