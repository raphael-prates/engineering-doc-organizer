import streamlit as st
from core.standard_extractor import receive_input, extract_pattern, save_standard, list_standards, delete_standard, load_standard

def render():
    # Initialize session state variables on first load
    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ''

    if 'upload_key' not in st.session_state:
        st.session_state['upload_key'] = 0

    if 'text_key' not in st.session_state:
        st.session_state['text_key'] = 0

    if 'patterns' not in st.session_state:
        st.session_state['patterns'] = None
    
    if 'selected_standard' not in st.session_state:
        st.session_state['selected_standard'] = None

    # ── Saved Standards section ─────────────────────────────────────────────
    st.subheader('Saved Standards')
    saved = list_standards()

    if saved:
        # Build display dict: "name — pattern" → name
        standards_dict = {}
        for name in saved:
            data = load_standard(name)
            standards_dict[f"{name} — {data['pattern']}"] = name

        col1, col2 = st.columns([3, 1])
        with col1:
            # Show selectbox with last saved standard selected by default
            saved_names = list(standards_dict.values())
            default_index = saved_names.index(st.session_state['selected_standard']) if st.session_state['selected_standard'] in saved_names else 0
            selected = st.selectbox('Select a standard', list(standards_dict.keys()), label_visibility='collapsed', index=default_index)
        with col2:
            # Delete selected standard and reset selection
            if st.button('Delete', use_container_width=True):
                delete_standard(standards_dict[selected])
                st.session_state['selected_standard'] = None
                st.rerun()
    else:
        st.write('No standard saved yet.')

    st.divider()

    # ── Pattern input section ───────────────────────────────────────────────
    st.subheader('File Pattern Config')
    # Dynamic keys allow programmatic clearing of inputs
    text_input = st.text_area('Paste the naming standard here: ', key=f'input_text_{st.session_state["text_key"]}')
    file_input = st.file_uploader('Or upload a .txt file', type=['txt'], key=st.session_state['upload_key'])

    col1, col2 = st.columns([1, 1])
    with col1:
        config_button = st.button('Search for Patterns', use_container_width=True)
    with col2:
        # Clear all inputs and found patterns
        if st.button('Clear', use_container_width=True):
            st.session_state['text_key'] += 1
            st.session_state['upload_key'] += 1
            st.session_state['patterns'] = None
            st.rerun()

    # ── Process input when Search is clicked ───────────────────────────────
    if config_button:
        if not text_input and not file_input:
            st.error('Please paste a text or upload a file.')
        else:
            patterns = None
            # Process text input
            if text_input:
                text = receive_input(text_input)
                patterns = extract_pattern(text)
            # Process file input — read bytes and decode to string
            if file_input:
                raw = file_input.read()
                text = receive_input(raw)
                patterns = extract_pattern(text)
            # Store found patterns or show error
            if patterns:
                st.session_state['patterns'] = patterns
            else:
                st.error('No patterns found. Make sure your text contains a naming pattern')

    # ── Pattern selection and save section ─────────────────────────────────
    if st.session_state['patterns']:
        patterns = st.session_state['patterns']
        # If multiple patterns found, let user choose
        if len(patterns) > 1:
            option = st.selectbox("Patterns found: ", patterns)
        else:
            option = patterns[0]
        st.write('')
        st.write('Selected Pattern: ', option)
        pattern_name = st.text_input('Enter a name for chosen pattern: ')

        if st.button('Save Pattern', use_container_width=True):
            # Validate: name required
            if pattern_name == '':
                st.error('Enter valid name!')
            # Validate: name must be unique
            elif pattern_name in list_standards():
                st.error('Chosen name already exists. Enter a valid name!')
            else:
                # Save, update selection, clear inputs and reload
                save_standard(option, pattern_name)
                st.session_state['selected_standard'] = pattern_name
                st.session_state['patterns'] = None
                st.session_state['text_key'] += 1
                st.session_state['upload_key'] += 1
                st.rerun()