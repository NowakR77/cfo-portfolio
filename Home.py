import streamlit as st


st.set_page_config(
    page_title="CFO & Builder",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Home Page Content
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

st.divider()
st.caption("📍 Currently building in Python, Streamlit, and n8n.")

st.divider()

# SaaS Metrics Calculator
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

# Sensitivity Analysis Table
st.divider()
st.subheader("Sensitivity Analysis")
st.caption("How does the Rule of 40 change if ARR growth drops by 5% increments?")

sensitivity_data = []
for drop in range(0, 26, 5):
    adj_growth = arr_growth - drop
    adj_rule = adj_growth + fcf_margin
    if adj_rule >= 40:
        rating = "Elite"
    elif adj_rule >= 20:
        rating = "Moderate"
    else:
        rating = "Needs Focus"
    sensitivity_data.append({
        "Growth Scenario": f"{adj_growth:+.1f}%" if drop > 0 else f"{adj_growth:.1f}% (Current)",
        "Growth Drop": f"-{drop}pp" if drop > 0 else "Baseline",
        "FCF Margin": f"{fcf_margin:.1f}%",
        "Rule of 40": f"{adj_rule:.1f}%",
        "vs. Target": f"{adj_rule - 40:+.1f}pp",
        "Rating": rating,
    })

st.dataframe(sensitivity_data, use_container_width=True, hide_index=True)
