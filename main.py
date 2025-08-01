
import streamlit as st
# updated input handling
def gauge_to_inches():
    user_input = input("Enter gauge: ")
    
    # Normalize curly quotes and remove spaces
    cleaned_input = (
        user_input
        .replace('’', "'")  # curly apostrophe to normal
        .replace('“', '"')  # curly double quote to normal
        .replace('”', '"')  # curly double quote to normal
        .replace('"', '')   # remove straight quotes
        .replace(' ', '')   # remove spaces
    )
    
    parsed_input = cleaned_input.split("'")
    if len(parsed_input) != 2:
        print("Invalid gauge format. Please use format like 10'6\".")
        return gauge_to_inches()
    
    feet = int(parsed_input[0])
    inches = int(parsed_input[1])
    total_inches = feet * 12 + inches
    return total_inches


def inches_to_bbl(inches):
    return inches * 1.66666667

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

    total_yest_water += yest_bot
    total_today_water += today_bot
    total_yest_oil += yest_top - yest_bot
    total_today_oil += today_top - today_bot

water_hauled = st.number_input("Barrels of water hauled in the past 24 hours:", min_value=0.0, step=1.0)
oil_hauled = st.number_input("Barrels of oil hauled in the past 24 hours:", min_value=0.0, step=1.0)

adjusted_water = total_today_water + water_hauled
adjusted_oil = total_today_oil + oil_hauled

final_water = adjusted_water - total_yest_water
final_oil = adjusted_oil - total_yest_oil

if st.button("Calculate"):
    st.success(f"Water Production: {round(final_water, 1)} bbls")
    st.success(f"Oil Production: {round(final_oil, 1)} bbls")
