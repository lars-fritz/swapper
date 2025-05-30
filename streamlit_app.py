import streamlit as st
import numpy as np

st.title("🔄 Uniswap V3 Swap Simulator")

# --- Constants and Defaults ---
default_p_min = 0.01
default_p_max = 0.06
default_amount_x = 10_000_000.0
default_x_out = 9_000_000.0
total_supply_x = 1_000_000_000  # For market cap calculation

st.header("1️⃣ Initialize Liquidity Position")

p_min = st.number_input("Minimum Price (Y per X)", value=float(default_p_min), min_value=0.000001, step=0.001, format="%.5f")
p_max = st.number_input("Maximum Price (Y per X)", value=float(default_p_max), min_value=0.000001, step=0.001, format="%.5f")

p_current = p_min
amount_x = st.number_input("Amount of Token X", value=float(default_amount_x), min_value=0.0, step=1.0)

if not (p_min < p_max):
    st.error("⚠️ p_min must be less than p_max.")
else:
    sqrt_p = np.sqrt(p_current)
    sqrt_p_min = np.sqrt(p_min)
    sqrt_p_max = np.sqrt(p_max)

    if sqrt_p >= sqrt_p_max:
        st.error("⚠️ Current price must be less than sqrt(p_max).")
    else:
        # Calculate liquidity
        L = amount_x / (1 / sqrt_p - 1 / sqrt_p_max)
        x_start = L * (1 / sqrt_p - 1 / sqrt_p_max)
        y_start = L * (sqrt_p - sqrt_p_min)

        # Current market price
        price = p_current
        market_cap = price * total_supply_x

        st.success(f"✅ Liquidity L: {L:.4f}")
        st.write(f"📊 Token X in pool: {x_start:,.2f}")
        st.write(f"📊 Token Y in pool: {y_start:,.2f}")
        st.write(f"💸 Market Price: {price:.5f}")
        st.write(f"🏦 Market Cap: {market_cap:,.2f} (supply = {total_supply_x:,})")

        # --- Single Swap Section ---
        st.header("2️⃣ Single Swap to Receive Token X")

        x_out = st.number_input(
            "Amount of Token X to Swap Out",
            min_value=0.0,
            max_value=float(x_start),
            value=float(default_x_out),
            step=1.0
        )

        if 0 < x_out < x_start:
            x_final = x_start - x_out
            inv_sqrt_p_final = (x_final / L) + (1 / sqrt_p_max)
            sqrt_p_final = 1 / inv_sqrt_p_final
            p_final = sqrt_p_final**2

            y_final = L * (sqrt_p_final - sqrt_p_min)
            y_in = y_final - y_start
            market_cap_new = p_final * total_supply_x

            st.subheader("📈 Result After Swap")
            st.write(f"✅ Final Price: {p_final:.5f}")
            st.write(f"💰 Y Required: {y_in:,.2f}")
            st.write(f"🏦 Final Market Cap: {market_cap_new:,.2f}")

        # --- Sequential Buys Section ---
        st.header("3️⃣ Simulate 3 Sequential Token X Buys")

        col1, col2, col3 = st.columns(3)
        buy1 = col1.number_input("Buy 1 (X tokens)", min_value=0.0, value=1_000_000.0, step=1.0)
        buy2 = col2.number_input("Buy 2 (X tokens)", min_value=0.0, value=1_000_000.0, step=1.0)
        buy3 = col3.number_input("Buy 3 (X tokens)", min_value=0.0, value=1_000_000.0, step=1.0)

        x_temp = x_start
        y_temp = y_start
        sqrt_p_temp = sqrt_p

        def apply_buy(x_reserve, y_reserve, sqrt_p_start, x_buy):
            x_new = x_reserve - x_buy
            inv_sqrt_p_new = (x_new / L) + (1 / sqrt_p_max)
            sqrt_p_new = 1 / inv_sqrt_p_new
            y_new = L * (sqrt_p_new - sqrt_p_min)
            y_in = y_new - y_reserve
            return x_new, y_new, sqrt_p_new, y_in

        y_in_total = 0
        for i, buy in enumerate([buy1, buy2, buy3], 1):
            if buy > x_temp:
                st.warning(f"⚠️ Buy {i} exceeds available X.")
                break
            x_temp, y_temp, sqrt_p_temp, y_in = apply_buy(x_temp, y_temp, sqrt_p_temp, buy)
            y_in_total += y_in

        final_price = sqrt_p_temp**2
        final_market_cap = final_price * total_supply_x

        st.subheader("📊 Result After 3 Sequential Buys")
        st.write(f"🪙 Final Token X: {x_temp:,.2f}")
        st.write(f"💸 Final Token Y: {y_temp:,.2f}")
        st.write(f"✅ Final Price: {final_price:.5f}")
        st.write(f"🏦 Final Market Cap: {final_market_cap:,.2f}")
        st.write(f"🧾 Total Y Spent: {y_in_total:,.2f}")
