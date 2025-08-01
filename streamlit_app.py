import streamlit as st

# --- Convert gauge format (e.g. 10'6" or 10’6”) to inches ---
def gauge_to_inches(prompt):
    user_input = st.text_input(prompt, key=prompt)
    if not user_input:
        st.stop()

    # Normalize various quote formats
    cleaned_input = (
        user_input
        .replace('’', "'")
        .replace('‘', "'")
        .replace('“', '"')
        .replace('”', '"')
        .replace('"', '')  # remove inches marker
        .replace(' ', '')  # remove spaces
    )

    try:
        feet, inches = cleaned_input.split("'")
        total_inches = int(feet) * 12 + int(inches)
        return total_inches
    except Exception:
        st.error("Invalid gauge format. Use format like 10'6\" or 8'0\".")
        st.stop()

# --- Convert inches to barrels (assumes 1 inch = 1.66666667 bbls) ---
def inches_to_bbl(total_inches):
    return total_inches * 1.66666667

# --- Streamlit App Starts Here ---
st.title("Fluid Production Calculator")

num_tanks = st.number_input("How many tanks are active?", min_value=1, step=1)

total_bbls = 0

for i in range(1, num_tanks + 1):
    st.header(f"Tank {i}")

    yest_top = inches_to_bbl(gauge_to_inches(f"Yesterday's top gauge for Tank {i}:"))
    yest_bottom = inches_to_bbl(gauge_to_inches(f"Yesterday's bottom gauge for Tank {i}:"))

    today_top = inches_to_bbl(gauge_to_inches(f"Today's top gauge for Tank {i}:"))
    today_bottom = inches_to_bbl(gauge_to_inches(f"Today's bottom gauge for Tank {i}:"))

    yest_total = yest_top - yest_bottom
    today_total = today_top - today_bottom
    production = today_total - yest_total

    st.success(f"Tank {i} production: {round(production, 2)} bbls")
    total_bbls += production

st.subheader(f"Total production across all tanks: {round(total_bbls, 2)} bbls")
