import streamlit as st

import pages.playground as pg

st.write("hello world")

page_chosen = "playground"

if page_chosen == "playground":
    pg.main()