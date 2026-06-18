import streamlit as st

st.set_page_config(page_title="Engineering Document Organizer", layout="wide")

PAGES = {
    "Config": "ui/pages/config_page.py",
    "Folder": "ui/pages/folder_page.py",
    "Scan": "ui/pages/scan_page.py",
    "Review": "ui/pages/review_page.py",
    "Apply": "ui/pages/apply_page.py",
}

with st.sidebar:
    st.title("Eng Doc Organizer")
    st.markdown("---")
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

st.header(page)

if page == "Config":
    st.info("Config page — coming soon.")
elif page == "Folder":
    st.info("Folder page — coming soon.")
elif page == "Scan":
    st.info("Scan page — coming soon.")
elif page == "Review":
    st.info("Review page — coming soon.")
elif page == "Apply":
    st.info("Apply page — coming soon.")
