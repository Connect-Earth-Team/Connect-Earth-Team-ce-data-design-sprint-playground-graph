import pandas as pd
import streamlit as st

import utils.display as display
import utils.inputs as inputs

data_raw = pd.read_csv("data/elec_consumption.csv")

def main():
    st.title("Playgrounnnndddd")

    st.title("Inputs")
    inputs.main()

    st.title("Display")
    display.main()




if __name__ == "__main__":
    main()