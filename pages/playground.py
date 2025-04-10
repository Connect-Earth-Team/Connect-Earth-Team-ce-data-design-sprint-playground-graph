import pandas as pd
import streamlit as st

import utils.display as display
import utils.inputs as inputs

data_raw = pd.read_csv("data/elec_consumption.csv", index_col=0)

st.dataframe(data_raw)

def main():
    st.title("Playgrounnnndddd")

    st.title("Inputs")
    inputs.main(data_raw=data_raw)

    st.title("Display")
    display.main()




if __name__ == "__main__":
    main()