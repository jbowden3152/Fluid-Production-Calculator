import streamlit as st

st.title("Oil & Water Production Calculator")

# Define a function that converts gauge input into total inches
def gauge_to_inches(prompt):
    user_input = st.text_input(prompt, key=prompt)
    if not user_input:
        st.stop()  # pause Streamlit until input is given
    cleaned_input = (
        user_input.replace('’', "'")
        .replace('“', '"')
        .replace('”', '"')
        .replace('"', '')
        .replace(' ', '')
    )
    try:
        feet, inches = cleaned_input.split("'")
        total_inches = int(feet) * 12 + int(inches)
        return total_inches
    except Exception:
        st.error("Invalid gauge format. Use format like 10'6\" or 8'0\".")
        st.stop()

# Ask for tank count
tank_count = st.number_input("How many tanks are actively being produced into?", min_value=1, step=1)

if tank_count:
    total_yest_water = 0
    total_yest_oil = 0
    total_today_water = 0
    total_today_oil = 0

    for i in range(1, tank_count + 1):
        st.subheader(f"Tank {i}")

        yest_top = inches_to_bbl(gauge_to_inches(f"Yesterday's top gauge for Tank {i}:"))
        yest_bot = inches_to_bbl(gauge_to_inches(f"Yesterday's bottom gauge for Tank {i}:"))
        today_top = inches_to_bbl(gauge_to_inches(f"Today's top gauge for Tank {i}:"))
        today_bot = inches_to_bbl(gauge_to_inches(f"Today's bottom gauge for Tank {i}:"))

        yest_oil = yest_top - yest_bot
        today_oil = today_top - today_bot

        total_yest_water += yest_bot
        total_today_water += today_bot
        total_yest_oil += yest_oil
        total_today_oil += today_oil

    water_hauled = st.number_input("How many barrels of water were hauled in the past 24 hours?", step=0.1)
    oil_hauled = st.number_input("How many barrels of oil were hauled in the past 24 hours?", step=0.1)

    if st.button("Calculate Production"):
        adjusted_water = total_today_water + water_hauled
        adjusted_oil = total_today_oil + oil_hauled

        final_water = round(adjusted_water - total_yest_water, 1)
        final_oil = round(adjusted_oil - total_yest_oil, 1)

        st.success(f"💧 Water Production: {final_water} bbls")
        st.success(f"🛢️ Oil Production: {final_oil} bbls")
