import streamlit as st
from ui.pages import config_page, folder_page, scan_page, review_page, apply_page

st.set_page_config(page_title="Eng Doc Organizer", layout='wide')
st.title('Engineering Document Organizer')

with st.sidebar:
    sidebar = st.radio('Main Functions', ['File Pattern Config', 'Directory Structure', 
                                'Scanner', 'Review', 'Reorganize'])
if sidebar == 'File Pattern Config':
    config_page.render()
elif sidebar == 'Directory Structure':
    folder_page.render()
elif sidebar == 'Scanner':
    scan_page.render()
elif sidebar == 'Review':
    review_page.render()
elif sidebar == 'Reorganize':
    apply_page.render()
 