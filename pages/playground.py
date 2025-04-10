import pandas as pd
import streamlit as st

import utils.display as display
import utils.inputs as inputs

data_raw = pd.read_csv("data/elec_consumption.csv", index_col=0)

def main():
    st.title("Playgrounnnndddd")

    data_modified = inputs.main(data_raw=data_raw)

    display.main(data_modified)




if __name__ == "__main__":
    main()