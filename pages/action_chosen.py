import utils.display as display
import streamlit as st


def main():
    # Set page config
    st.set_page_config(
        page_title="Action Chosen",
        layout="centered",
        page_icon="🌍",
        initial_sidebar_state="collapsed",
    )
    st.session_state["current_page"] = 'action chosen'

    display.main()


if __name__ == "__main__":
    main()