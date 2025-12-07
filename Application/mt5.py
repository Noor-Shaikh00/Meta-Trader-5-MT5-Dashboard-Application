# Mini Trading Dashboard - MT5 Style
# Developed by Noor Shaikh

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Mini Trading Dashboard", page_icon="💹", layout="wide")
st.title("🌐 Mini Trading Dashboard")
st.markdown("Welcome Trader! 📊 Practice your trading skills here.")

# ------------------------
# Initial Setup
# ------------------------
if 'balance' not in st.session_state:
    st.session_state.balance = 10000  # starting balance
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}  # {'AAPL': quantity}
if 'history' not in st.session_state:
    st.session_state.history = []  # list of transactions

# ------------------------
# Asset Data (Simulated)
# ------------------------
assets = {
    "USD/EUR": 1.12,
    "BTC/USD": 60000,
    "AAPL": 175,
    "GOLD": 1800
}

def get_price(asset):
    # simulate small random fluctuations
    base_price = assets[asset]
    price = round(base_price * (1 + random.uniform(-0.02, 0.02)), 2)
    return price

# ------------------------
# Display Balance
# ------------------------
st.subheader("💰 Account Balance & Portfolio")
st.metric(label="Current Balance", value=f"${st.session_state.balance:,.2f}")

# Calculate portfolio value
portfolio_value = 0
for asset, qty in st.session_state.portfolio.items():
    portfolio_value += qty * get_price(asset)
st.metric(label="Portfolio Value", value=f"${portfolio_value:,.2f}")

# ------------------------
# Trading Section
# ------------------------
st.subheader("💹 Trade Assets")

col1, col2, col3 = st.columns([2,2,2])

with col1:
    selected_asset = st.selectbox("Select Asset", list(assets.keys()))

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1)

current_price = get_price(selected_asset)
st.write(f"Current Price of {selected_asset}: ${current_price}")

col4, col5 = st.columns([1,1])

with col4:
    if st.button("Buy"):
        cost = quantity * current_price
        if st.session_state.balance >= cost:
            st.session_state.balance -= cost
            st.session_state.portfolio[selected_asset] = st.session_state.portfolio.get(selected_asset,0) + quantity
            st.session_state.history.append(f"Bought {quantity} {selected_asset} at ${current_price}")
            st.success(f"✅ Bought {quantity} {selected_asset} for ${cost}")
        else:
            st.error("❌ Not enough balance!")

with col5:
    if st.button("Sell"):
        if st.session_state.portfolio.get(selected_asset,0) >= quantity:
            st.session_state.portfolio[selected_asset] -= quantity
            revenue = quantity * current_price
            st.session_state.balance += revenue
            st.session_state.history.append(f"Sold {quantity} {selected_asset} at ${current_price}")
            st.success(f"✅ Sold {quantity} {selected_asset} for ${revenue}")
        else:
            st.error("❌ Not enough quantity in portfolio!")

# ------------------------
# Portfolio Table
# ------------------------
st.subheader("📋 Portfolio Details")
if st.session_state.portfolio:
    portfolio_df = pd.DataFrame({
        "Asset": list(st.session_state.portfolio.keys()),
        "Quantity": list(st.session_state.portfolio.values()),
        "Current Price": [get_price(a) for a in st.session_state.portfolio.keys()],
    })
    portfolio_df["Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]
    st.dataframe(portfolio_df)
else:
    st.info("Portfolio is empty. Buy some assets!")

# ------------------------
# Price Chart
# ------------------------
st.subheader("📈 Price Chart")

# Simulate price history
time_series = pd.date_range(end=pd.Timestamp.today(), periods=30)
price_series = [round(get_price(selected_asset)*(1 + random.uniform(-0.05,0.05)),2) for _ in range(30)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=time_series, y=price_series, mode='lines+markers', name=selected_asset))
fig.update_layout(title=f"Price Trend for {selected_asset}", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Transaction History
# ------------------------
st.subheader("📝 Transaction History")
if st.session_state.history:
    for tx in reversed(st.session_state.history[-10:]):
        st.write(f"- {tx}")
else:
    st.info("No transactions yet.")

# ------------------------
# Top Movers (Simulated)
# ------------------------
st.subheader("🔥 Top Movers Today")
top_movers = {asset: round(random.uniform(-5,5),2) for asset in assets.keys()}
top_movers_df = pd.DataFrame({
    "Asset": list(top_movers.keys()),
    "% Change": [f"{val}% {'📈' if val>0 else '📉'}" for val in top_movers.values()]
})
st.dataframe(top_movers_df)

# ------------------------
# Footer
# ------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("✨ Developed by Noor Shaikh ✨")
