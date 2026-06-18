"""
Config page — naming standard configuration.

Lets the user select a naming standard (OTTS-016 or custom), configure
company/terminal codes, and save preferences that persist across sessions.
"""

import os
import streamlit as st
from core.standard_extractor import extract, save_standard, load_standard

STANDARDS_DIR = "config/standards"

_TYPE_LABELS = {
    "numeric":      "Numeric  (\\d)",
    "alpha":        "Alpha  ([A-Z] / [a-z])",
    "revision":     "Revision  ([A-Za-z0-9])",
    "alphanumeric": "Alphanumeric  ([A-Za-z0-9])",
}

_NO_SELECTION = "-- select a standard --"


def _list_standards() -> list[str]:
    """Return sorted list of JSON filenames (without extension) in STANDARDS_DIR."""
    try:
        return sorted(
            os.path.splitext(f)[0]
            for f in os.listdir(STANDARDS_DIR)
            if f.endswith(".json")
        )
    except FileNotFoundError:
        return []


def _close_form():
    st.session_state["cfg_form_open"] = False
    st.session_state["cfg_parsed"] = None
    st.session_state["cfg_parse_error"] = None


def render():
    st.subheader("Naming Standard")

    standards = _list_standards()
    options = [_NO_SELECTION] + standards

    # ── Top controls ────────────────────────────────────────────────────────
    col_select, col_btn = st.columns([4, 1])
    with col_select:
        selected = st.selectbox(
            "Saved standards",
            options,
            index=0,
            label_visibility="collapsed",
            key="cfg_selected",
        )
    with col_btn:
        if st.button("New pattern", use_container_width=True):
            st.session_state["cfg_form_open"] = True
            st.session_state["cfg_parsed"] = None
            st.session_state["cfg_parse_error"] = None

    # ── Selected standard detail ─────────────────────────────────────────────
    if selected != _NO_SELECTION:
        path = os.path.join(STANDARDS_DIR, f"{selected}.json")
        data = load_standard(path)
        if data:
            st.markdown("---")
            st.markdown(f"**Pattern:** `{data.get('pattern', '(unknown)')}`")
            st.markdown(f"**Regex:** `{data.get('regex', '(unknown)')}`")
            if st.button("Delete", type="secondary", key="cfg_delete"):
                try:
                    os.remove(path)
                    st.rerun()
                except OSError as exc:
                    st.error(f"Could not delete: {exc}")

    # ── Creation form ────────────────────────────────────────────────────────
    if not st.session_state.get("cfg_form_open"):
        return

    st.markdown("---")
    st.markdown(
        "Placeholder conventions: `0` → numeric digit · "
        "`X` → uppercase alpha · `x` → lowercase alpha · "
        "`rev00` / `revXX` → revision suffix  \n"
        "**Example:** `00-000-XXX-XXX-000-0000.revXX`"
    )

    with st.form("cfg_pattern_form"):
        name = st.text_input("Standard name", placeholder="my_project")
        pattern = st.text_input(
            "Naming pattern",
            placeholder="00-000-XXX-XXX-000-0000.revXX",
        )
        submitted = st.form_submit_button("Parse Pattern", type="primary")

    if submitted:
        if not name.strip() or not pattern.strip():
            st.session_state["cfg_parsed"] = None
            st.session_state["cfg_parse_error"] = "Please fill in both the standard name and the pattern."
        else:
            try:
                result = extract(pattern)
                result["name"] = name.strip()
                st.session_state["cfg_parsed"] = result
                st.session_state["cfg_parse_error"] = None
            except ValueError as exc:
                st.session_state["cfg_parsed"] = None
                st.session_state["cfg_parse_error"] = str(exc)

    if st.session_state.get("cfg_parse_error"):
        st.error(st.session_state["cfg_parse_error"])

    parsed = st.session_state.get("cfg_parsed")
    if not parsed:
        _, col_cancel = st.columns([4, 1])
        with col_cancel:
            if st.button("Cancel", use_container_width=True, key="cfg_cancel_empty"):
                _close_form()
                st.rerun()
        return

    # ── Parsed result ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Parsed segments")

    rows = []
    for seg in parsed["segments"]:
        sep_display = repr(seg["separator_after"]) if seg["separator_after"] else "—"
        rows.append({
            "#":           seg["index"] + 1,
            "Placeholder": seg["placeholder"],
            "Type":        _TYPE_LABELS.get(seg["type"], seg["type"]),
            "Length":      seg["length"],
            "Separator":   sep_display,
        })
    st.table(rows)

    st.markdown("#### Generated regex")
    st.code(parsed["regex"], language="")

    st.markdown("---")
    col_save, col_cancel = st.columns([1, 1])
    with col_save:
        if st.button("Confirm & Save", type="primary", use_container_width=True):
            dest = os.path.join(STANDARDS_DIR, f"{parsed['name']}.json")
            try:
                save_standard(parsed, dest)
                _close_form()
                st.rerun()
            except OSError as exc:
                st.error(f"Could not save: {exc}")
    with col_cancel:
        if st.button("Cancel", use_container_width=True, key="cfg_cancel"):
            _close_form()
            st.rerun()
