import streamlit as st
import numpy as np

st.title("🔄 Uniswap V3 Swap Calculator (Token X Only)")

# --- Default parameters ---
default_p_min = 0.01
default_p_max = 0.06
default_p_current = default_p_min
default_amount_x = 10_000_000.0
default_x_out = 9_000_000.0

# Step 1: Initialize liquidity
st.header("1️⃣ Initialize Liquidity Position")

p_min = st.number_input("Minimum Price (Y per X)", value=float(default_p_min), min_value=0.000001, step=0.001, format="%.5f")
p_max = st.number_input("Maximum Price (Y per X)", value=float(default_p_max), min_value=0.000001, step=0.001, format="%.5f")

# Automatically set p_current = p_min
p_current = p_min
st.markdown(f"**Current price is set to p_min = {p_current:.5f}**")

amount_x = st.number_input("Amount of Token X", value=float(default_amount_x), min_value=0.0, step=1.0)

# Check that p_min < p_max
if not (p_min < p_max):
    st.error("⚠️ p_min must be less than p_max.")
else:
    sqrt_p = np.sqrt(p_current)
    sqrt_p_min = np.sqrt(p_min)
    sqrt_p_max = np.sqrt(p_max)

    if sqrt_p >= sqrt_p_max:
        st.error("⚠️ Current price must be less than sqrt(p_max).")
    else:
        # Compute liquidity L from x only
        L = amount_x / (1 / sqrt_p - 1 / sqrt_p_max)
        x_start = L * (1 / sqrt_p - 1 / sqrt_p_max)
        y_start = L * (sqrt_p - sqrt_p_min)

        st.success(f"✅ Calculated Liquidity L: {L:.4f}")
        st.write(f"📊 Initial Token X: {x_start:,.2f}")
        st.write(f"📊 Initial Token Y: {y_start:,.2f}")

        # Step 2: Simulate swap
        st.header("2️⃣ Swap to Receive Token X")

        x_out = st.number_input(
            "Desired amount of Token X (x_out)",
            min_value=0.0,
            max_value=float(x_start),
            value=float(default_x_out),
            step=1.0
        )

        if x_out >= x_start:
            st.warning("⚠️ Not enough X available for the requested swap.")
        elif x_out > 0:
            x_final = x_start - x_out
            inv_sqrt_p_final = (x_final / L) + (1 / sqrt_p_max)
            sqrt_p_final = 1 / inv_sqrt_p_final
            p_final = sqrt_p_final**2

            y_final = L * (sqrt_p_final - sqrt_p_min)
            y_in = y_final - y_start

            st.subheader("📈 Swap Result")
            st.write(f"✅ Final price after swap: {p_final:.5f} (√p = {sqrt_p_final:.5f})")
            st.write(f"💰 Required Token Y input: **{y_in:,.2f}**")
            st.write(f"Remaining Token X in pool: {x_final:,.2f}")

