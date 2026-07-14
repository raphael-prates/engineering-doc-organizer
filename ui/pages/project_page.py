import os
import streamlit as st
from core.project_manager import save_project, load_project, list_projects, delete_project

def render():
    # Initialize session state variables on first load
    if 'project_name' not in st.session_state:
        st.session_state['project_name'] = ''
    if 'project_year' not in st.session_state:
        st.session_state['project_year'] = ''
    if 'project_path' not in st.session_state:
        st.session_state['project_path'] = ''
    if 'selected_project' not in st.session_state:
        st.session_state['selected_project'] = None
    if 'year_key' not in st.session_state:
        st.session_state['year_key'] = 0
    if 'path_key' not in st.session_state:
        st.session_state['path_key'] = 0
    if 'name_key' not in st.session_state:
        st.session_state['name_key'] = 0

    # ── Saved projects section ─────────────────────────────────────────────
    st.subheader('Saved Projects')
    saved = list_projects()

    if saved:
        # Build display dict: "name — year" → name
        projects_dict = {}
        for name in saved:
            data = load_project(name)
            projects_dict[f"{name} — {data['year']}"] = name

        col1, col2 = st.columns([3, 1])
        with col1:
            # Show selectbox with last saved project selected by default
            saved_projects = list(projects_dict.values())
            default_index = saved_projects.index(
                st.session_state['selected_project']) if st.session_state['selected_project'] in saved_projects else 0
            selected = st.selectbox('Select a project', list(
                projects_dict.keys()), label_visibility='collapsed', index=default_index)
        with col2:
            # Delete selected project and reset selection
            if st.button('Delete', use_container_width=True):
                delete_project(projects_dict[selected])
                st.session_state['selected_project'] = None
                st.rerun()
    else:
        st.write('No projects saved yet.')

    st.divider()

    # ── New project input section ───────────────────────────────────────────
    st.subheader('New Project')
    st.write(
        'Enter the project name, year and the path to the folder containing the files.')

    # Dynamic keys allow programmatic clearing of inputs
    project_name = st.text_input(
        'Project Name:', key=f'name_input_{st.session_state["name_key"]}')
    project_year = st.text_input(
        'Project Year:', key=f'year_input_{st.session_state["year_key"]}', placeholder='Ex: 2025')
    project_path = st.text_input(
        'Project Path:', key=f'path_input_{st.session_state["path_key"]}', placeholder='Ex: C:\\Users\\Pratz\\Documents\\2025 - Reforço Estrutural')

    col1, col2 = st.columns([1, 1])
    with col1:
        save_button = st.button('Save Project', use_container_width=True)
    with col2:
        # Clear all inputs
        if st.button('Clear', use_container_width=True):
            st.session_state['name_key'] += 1
            st.session_state['year_key'] += 1
            st.session_state['path_key'] += 1
            st.rerun()

    # ── Validate and save when button is clicked ───────────────────────────
    if save_button:
        # Validate: all fields required
        if not project_name or not project_year or not project_path:
            st.error('All fields are required.')
        # Validate: project name must be unique
        elif project_name in list_projects():
            st.error('Project name already exists. Enter a different name.')
        # Validate: path must exist on disk
        elif not os.path.exists(project_path):
            st.error('Path not found. Make sure the folder exists.')
        else:
            # Save project and update selection
            save_project(project_name, project_year, project_path)
            st.session_state['selected_project'] = project_name
            st.session_state['name_key'] += 1
            st.session_state['year_key'] += 1
            st.session_state['path_key'] += 1
            st.rerun()
