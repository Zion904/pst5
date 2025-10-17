# main.py
import streamlit as st
from gui.main_dashboard import launch
# Import the new admin utilities.
from app.admin_utils import init_logger, backup_data

if __name__ == "__main__":
    # Initialize the logger as the very first step.
    if "booted" not in st.session_state:
        init_logger("msms.log")                       
        backup_data("data/msms.json", "data/backups") 
        st.session_state.booted = True
        
    # Launch the GUI as before.
    launch()