import streamlit as st
import numpy as np

st.title("🔄 Uniswap V3 Swap Calculator (Token X Only)")

# Step 1: Initialize liquidity
st.header("1️⃣ Initialize Liquidity Position")

p_min = st.number_input("Minimum Price (Y per X)", value=1/3, min_value=0.00001, step=0.01, format="%.5f")
p_max = st.number_input("Maximum Price (Y per X)", value=3.0, min_value=0.00001, step=0.01, format="%.5f")
p_current = st.number_input("Current Price (Y per X)", value=1.0, min_value=p_min, max_value=p_max, step=0.01)
amount_x = st.number_input("Amount of Token X", value=5000.0, min_value=0.0)

sqrt_p = np.sqrt(p_current)
sqrt_p_min = np.sqrt(p_min)
sqrt_p_max = np.sqrt(p_max)

if sqrt_p >= sqrt_p_max:
    st.error("Current price must be less than sqrt(p_max).")
else:
    # Compute liquidity
    L = amount_x / (1 / sqrt_p - 1 / sqrt_p_max)
    x_start = L * (1 / sqrt_p - 1 / sqrt_p_max)
    y_start = L * (sqrt_p - sqrt_p_min)

    st.success(f"Calculated Liquidity L: {L:.4f}")
    st.write(f"📊 Initial X: {x_start:.2f}, Initial Y: {y_start:.2f}")

    # Step 2: Simulate swap
    st.header("2️⃣ Swap to Receive Token X")

    x_out = st.number_input("Desired amount of Token X (x_out)", min_value=0.0, max_value=x_start, value=1000.0)

    if x_out >= x_start:
        st.warning("⚠️ Not enough X available for the requested swap.")
    elif x_out > 0:
        # Final X amount
        x_final = x_start - x_out

        # Solve for sqrt(p_final)
        inv_sqrt_p_final = (x_final / L) + (1 / sqrt_p_max)
        sqrt_p_final = 1 / inv_sqrt_p_final
        p_final = sqrt_p_final**2

        # Calculate y required
        y_final = L * (sqrt_p_final - sqrt_p_min)
        y_in = y_final - y_start

        st.subheader("📈 Swap Result")
        st.write(f"✅ Final price after swap: {p_final:.5f} (sqrt(p) = {sqrt_p_final:.5f})")
        st.write(f"💰 Required Token Y input: {y_in:.5f}")
        st.write(f"Remaining Token X in pool: {x_final:.2f}")
