import streamlit as st
import pandas as pd
import time

# ----------------------------
#   Page Config
# ----------------------------
st.set_page_config(
    page_title="ASC Elections Prediction Dashboard",
    page_icon="📊",
    layout="centered",
)

st.title("📊 ASC Elections Prediction Dashboard")
st.subheader("Predict who will win: Team Active vs Team New Wave")

st.write(
    """
    This is **not a betting platform**.  
    It's a fun analytical dashboard where students can **predict** 
    the outcome of the ASC elections without using money or betting.
    """
)

# ----------------------------
#   Initialize State
# ----------------------------
if "active_votes" not in st.session_state:
    st.session_state.active_votes = 0

if "newwave_votes" not in st.session_state:
    st.session_state.newwave_votes = 0

# ----------------------------
#   Voting Section
# ----------------------------
st.markdown("### 🗳 Submit Your Prediction")

choice = st.radio(
    "Who do you think will win?",
    ["Team Active", "Team New Wave"],
    horizontal=True
)

if st.button("Submit Prediction"):
    if choice == "Team Active":
        st.session_state.active_votes += 1
    else:
        st.session_state.newwave_votes += 1
    st.success("Prediction submitted!")

# ----------------------------
#   Results Section
# ----------------------------
st.markdown("### 📈 Live Prediction Results")

total = st.session_state.active_votes + st.session_state.newwave_votes
if total == 0:
    st.info("No predictions yet. Be the first one!")
else:
    active_pct = (st.session_state.active_votes / total) * 100
    newwave_pct = (st.session_state.newwave_votes / total) * 100

    st.write(f"**Total predictions:** {total}")

    results_df = pd.DataFrame({
        "Team": ["Team Active", "Team New Wave"],
        "Predictions (%)": [active_pct, newwave_pct],
        "Votes": [st.session_state.active_votes, st.session_state.newwave_votes]
    })

    st.bar_chart(results_df.set_index("Team")["Predictions (%)"])

    st.dataframe(results_df)

# ----------------------------
#   About Section
# ----------------------------
st.markdown("---")
st.markdown("### ℹ️ About This Dashboard")
st.write(
    """
    This tool is for **academic and entertainment purposes only**.  
    It tracks **predictions**, not bets, and does not involve real money.
    """
)
