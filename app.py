import utils.display as display
import streamlit as st

def main():
    st.session_state["current_page"] = 'app'
    display.main()


if __name__ == "__main__":
    main()