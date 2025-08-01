import streamlit as st

def gauge_to_inches(gauge_str):
    if not gauge_str or gauge_str.strip() == '':
        return 0
    
    # Replace common formatting issues: smart quotes, commas, spaces
    cleaned_input = (
        gauge_str.replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace(",", "")
        .replace('"', '')
        .replace(" ", '')
    )
    
    if "'" not in cleaned_input:
        return 0
    
    parsed_input = cleaned_input.split("'")
    
    if len(parsed_input) < 2 or not parsed_input[0] or not parsed_input[1]:
        return 0
    
    try:
        feet = int(parsed_input[0])
        inches = int(parsed_input[1])
        return feet * 12 + inches
    except ValueError:
        return 0

def inches_to_bbl(inches):
    return inches * 1.66666667

# -------------------------------
# STREAMLIT INTERFACE
# -------------------------------

st.title("Daily Fluid Production Calculator")

tank_count = st.number_input("How many tanks are actively being produced into?", min_value=1, step=1)

total_yest_water = 0
total_today_water = 0
total_yest_oil = 0
total_today_oil = 0

for i in range(1, tank_count + 1):
    st.subheader(f"Tank {i}")
    yest_top = inches_to_bbl(gauge_to_inches(st.text_input(f"Yesterday's top gauge (e.g. 5'8\") for Tank {i}")))
    yest_bot = inches_to_bbl(gauge_to_inches(st.text_input(f"Yesterday's bottom gauge (e.g. 3'4\") for Tank {i}")))
    today_top = inches_to_bbl(gauge_to_inches(st.text_input(f"Today's top gauge (e.g. 6'2\") for Tank {i}")))
    today_bot = inches_to_bbl(gauge_to_inches(st.text_input(f"Today's bottom gauge (e.g. 4'0\") for Tank {i}")))

    # Water is bottom gauge; Oil is top - bottom
    total_yest_water += yest_bot
    total_today_water += today_bot
    total_yest_oil += yest_top - yest_bot
    total_today_oil += today_top - today_bot

# Include barrels hauled
water_hauled = st.number_input("Barrels of water hauled in the past 24 hours:", min_value=0.0, step=1.0)
oil_hauled = st.number_input("Barrels of oil hauled in the past 24 hours:", min_value=0.0, step=1.0)

# Adjust current tanks by adding hauled fluid back in
adjusted_today_water = total_today_water + water_hauled
adjusted_today_oil = total_today_oil + oil_hauled

# Final 24-hour production calculations
final_water = adjusted_today_water - total_yest_water
final_oil = adjusted_today_oil - total_yest_oil

if st.button("Calculate"):
    st.success(f"Water Production: {round(final_water, 1)} bbls")
    st.success(f"Oil Production: {round(final_oil, 1)} bbls")
