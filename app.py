import streamlit as st

def estimate_option_price(current_price, delta, nifty_move_points, iv_spike_pct=0):
    intrinsic_gain = delta * nifty_move_points
    iv_boost = current_price * (iv_spike_pct / 100)
    estimated_price = current_price + intrinsic_gain + iv_boost
    return round(estimated_price, 2)

st.set_page_config(page_title="Option Price Estimator", page_icon="📈")
st.title("Nifty Option Price Estimator")

current_price = st.number_input("Current Option Price (₹)", min_value=1.0, value=10.0)
delta = st.slider("Option Delta", min_value=0.1, max_value=1.0, step=0.05, value=0.3)
nifty_move = st.number_input("Expected Nifty Move (points)", min_value=0, value=660)
iv_spike = st.slider("Expected IV Spike (%)", min_value=0, max_value=50, step=5, value=10)

if st.button("Estimate Opening Price"):
    estimated_price = estimate_option_price(current_price, delta, nifty_move, iv_spike)
    target_1 = round(estimated_price * 1.25, 2)
    target_2 = round(estimated_price * 1.5, 2)
    stop_loss = round(current_price * 0.75, 2)

    st.markdown("### Results")
    st.write(f"**Estimated Opening Price:** ₹{estimated_price}")
    st.write(f"**Target 1 (25% Profit):** ₹{target_1}")
    st.write(f"**Target 2 (50% Profit):** ₹{target_2}")
    st.write(f"**Stop-Loss (25% below entry):** ₹{stop_loss}")
