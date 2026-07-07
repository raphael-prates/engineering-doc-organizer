import streamlit as st
import os
from core.standard_extractor import receive_input, extract_pattern, save_standard, list_standards, delete_standard, load_standard

def render():
    if 'patterns' not in st.session_state:
        st.session_state['patterns'] = None
    st.subheader ('Saved Standards')
    saved = list_standards()

    if saved:
        standards_dict = {}
        for name in saved:
            data = load_standard(name)
            standards_dict[f"{name} — {data['pattern']}"] = name

        col1, col2 = st.columns([3,1])
        with col1:
            selected = st.selectbox('Select a standard', list(standards_dict.keys()), label_visibility='collapsed')
        with col2:
            if st.button('Delete', use_container_width=True):
                delete_standard(standards_dict[selected])
                st.rerun()
    else:
        st.write('No standard saved yet.')

    st.divider()

    st.subheader('File Pattern Config')
    text_input = st.text_area('Paste the naming standard here: ')
    file_input = st.file_uploader('Or upload a .txt file', type=['txt'])
    config_button = st.button('Search for Patterns')

    if config_button:
        patterns = None
        if text_input:
            text = receive_input(text_input)
            patterns = extract_pattern(text)
        if file_input:
            raw = file_input.read()
            text = receive_input(raw)
            patterns = extract_pattern(text)
        if patterns:
            st.session_state['patterns'] = patterns
        else:
            st.error('No patterns found. Make sure your text contains a naming pattern')

    if st.session_state['patterns']:
        patterns = st.session_state['patterns']
        if len(patterns) > 1:
            option = st.selectbox("Patterns found: ", patterns)
        else:
            option = patterns[0]
        st.write('')
        st.write('Selected Pattern: ', option)
        pattern_name = st.text_input('Enter a name for chosen pattern: ')
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button('Save Pattern', use_container_width=True):
                if pattern_name == '':
                    st.error('Enter valid name!')
                elif pattern_name in list_standards():
                    st.error('Chosen name already exist. Enter a valid name!')
                else:
                    save_standard(option, pattern_name)
                    st.success('Pattern saved!')
                    st.session_state['patterns'] = None
                    st.rerun()
        with col2:
            if st.button('Clear', use_container_width=True):
                st.session_state['patterns'] = None
                st.rerun()
