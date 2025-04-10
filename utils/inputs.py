import pandas as pd
import streamlit as st

N_PERIODS = 12

# Savings data
LIGHTING_SAVING = 0.05
SAVING_PER_SOLAR_PANEL = 0.1 # replace with array

# other data
ELEC_PRICE = 0.25 # £/kWh
ELEC_EMISSIONS = 0.3 # kg CO2e/kWh


def row_panel_input(input_func):
    with st.container(border=True, height=120):
        value = input_func()
    return value

def choose_inputs():
    n_inputs = 3
    INPUT_WIDTH = 0.35
    col_sizes = [INPUT_WIDTH] * n_inputs
    col_sizes.append(max(1 - n_inputs * INPUT_WIDTH, 0.001))
    columns = st.columns(col_sizes)
    with columns[0]:
        n_panels = row_panel_input(
            input_func=lambda: st.slider("☀️ **Number of Solar Panels:**", min_value=0, max_value=10, step=1, key="solar_panels")
        )
    with columns[1]:
        led = row_panel_input(
            input_func=lambda: st.toggle("💡 **Switch to LED Lighting:**", key="led_lighting")
        )
    with columns[2]:
        row_panel_input(
            input_func=lambda: st.toggle("👀 **Coming soon...**", key="electronics", disabled=True)
        )
        
    return [{"name": "solar_panels", "value": n_panels}, {"name": "led_lighting", "value": led}]

def apply_elec_consumption_reduction(consumption_values: list, reduction_pct: float):
    return [x * reduction_pct for x in consumption_values]

def calculate_solar_panels(n_panels: int):
    saving_all_panels = n_panels * SAVING_PER_SOLAR_PANEL
    consumption_multiplier = [(1-saving_all_panels)] * N_PERIODS
    return consumption_multiplier

def calculate_led_lighting(led_lighting: bool):
    savings = LIGHTING_SAVING if led_lighting else 0
    consumption_multiplier = [(1-savings)] * N_PERIODS # first version: same reduction for each month
    return consumption_multiplier

def combine_multipliers(multipliers: list) -> list:
    combined_multiplier = [1] * N_PERIODS
    for multiplier in multipliers:
        combined_multiplier = [total * new for total, new in zip(combined_multiplier, multiplier)]
    return combined_multiplier

def calculate_impact_of_modifiers(modifiers: list, data_raw: pd.DataFrame) -> pd.DataFrame:

    modified_data = data_raw.copy()

    multipliers = []
    for modifier in modifiers:
        match modifier["name"]:
            case "solar_panels":
                multipliers.append(calculate_solar_panels(modifier["value"]))
            case "led_lighting":
                multipliers.append(calculate_led_lighting(modifier["value"]))
    
    final_multipliers = combine_multipliers(multipliers=multipliers)

    modified_data["elec_consumption_modified"] = modified_data["elec_consumption_kwh"] * final_multipliers
    modified_data["elec_spend_modified_gbp"] = modified_data.elec_consumption_modified * ELEC_PRICE
    modified_data["elec_emissions_modified_kg_co2e"] = modified_data.elec_consumption_modified * ELEC_EMISSIONS

    return modified_data

def main(data_raw: pd.DataFrame) -> pd.DataFrame:
    inputs = choose_inputs()
    modified_data = calculate_impact_of_modifiers(modifiers=inputs, data_raw=data_raw)
    return modified_data