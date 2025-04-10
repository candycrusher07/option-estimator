import streamlit as st
from math import log, sqrt, exp
from scipy.stats import norm

# --- Black-Scholes Call Option Price ---
def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (log(S/K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    return round(call_price, 2), round(delta, 3)

# --- Auto IV spike estimator based on % change or events ---
def estimate_iv_spike(gift_nifty_change, event_type):
    spike = 0

    # Base estimate from GIFT Nifty % change
    if abs(gift_nifty_change) >= 3:
        spike += 0.25
    elif abs(gift_nifty_change) >= 2:
        spike += 0.18
    elif abs(gift_nifty_change) >= 1:
        spike += 0.12
    else:
        spike += 0.07

    # Adjust based on market event
    event_boost = {
        "None": 0.00,
        "RBI Policy": 0.05,
        "US CPI Data": 0.08,
        "Fed Meeting": 0.1,
        "Budget Day": 0.2,
        "Quarterly Results": 0.04
    }
    spike += event_boost.get(event_type, 0)

    return round(spike, 2)

# --- Streamlit App Interface ---
st.title("📈 Option Price Estimator with Auto IV Spike")

st.markdown("Get quick estimates of option prices and delta based on GIFT Nifty and expected IV changes.")

# Input: Current Spot Price
spot_price = st.number_input("Nifty Spot Price", value=22500)

# Input: Strike Price
strike_price = st.number_input("Option Strike Price", value=22700)

# Input: Time to Expiry (in Days)
days_to_expiry = st.slider("Days to Expiry", min_value=1, max_value=30, value=7)
T = days_to_expiry / 365

# Input: Risk-free interest rate
r = 0.06  # 6% assumed

st.subheader("📊 GIFT Nifty & Market Event")
gift_nifty_change = st.slider("GIFT Nifty % Change", min_value=-5.0, max_value=5.0, step=0.1, value=1.5)
event_type = st.selectbox("Market Event", ["None", "RBI Policy", "US CPI Data", "Fed Meeting", "Budget Day", "Quarterly Results"])

# Manual Override Toggle
manual_iv_toggle = st.toggle("Manually Override IV?", value=False)

# Implied Volatility
if manual_iv_toggle:
    implied_volatility = st.slider("Enter Implied Volatility (IV)", min_value=0.05, max_value=1.0, step=0.01, value=0.25)
else:
    estimated_iv = estimate_iv_spike(gift_nifty_change, event_type)
    implied_volatility = estimated_iv
    st.info(f"Estimated IV based on inputs: **{round(implied_volatility * 100, 2)}%**")

# Calculate Option Price and Delta
price, delta = black_scholes_call_price(spot_price, strike_price, T, r, implied_volatility)

# Display Outputs
st.success(f"💸 Estimated Option Price: ₹ {price}")
st.warning(f"📐 Delta: {delta}")

# Footer
st.caption("Built with ❤ by your custom trading assistant")

