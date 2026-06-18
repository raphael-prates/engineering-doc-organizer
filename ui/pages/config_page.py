"""
Config page — naming standard configuration.

Lets the user select a naming standard (OTTS-016 or custom), configure
company/terminal codes, and save preferences that persist across sessions.
"""

import streamlit as st
from core.standard_extractor import extract, save_standard, load_standard

CUSTOM_STANDARD_PATH = "config/standards/custom.json"

_TYPE_LABELS = {
    "numeric":      "Numeric  (\\d)",
    "alpha":        "Alpha  ([A-Z] / [a-z])",
    "revision":     "Revision  ([A-Za-z0-9])",
    "alphanumeric": "Alphanumeric  ([A-Za-z0-9])",
}


def render():
    st.subheader("Naming Standard")

    # ── Active custom standard ──────────────────────────────────────────────
    saved = load_standard(CUSTOM_STANDARD_PATH)
    if saved:
        st.success(f"Active custom standard: `{saved.get('pattern', '(unknown)')}`")
        with st.expander("View saved standard JSON"):
            st.json(saved)

    st.markdown("---")

    # ── Pattern input ───────────────────────────────────────────────────────
    st.markdown(
        "Paste a filename pattern using placeholders:\n"
        "- `0` — numeric digit\n"
        "- `X` — uppercase alpha character\n"
        "- `x` — lowercase alpha character\n"
        "- `rev00` or `revXX` — revision suffix\n\n"
        "**Example:** `00-000-XXX-XXX-000-0000.revXX`"
    )

    pattern = st.text_input(
        "Naming pattern",
        placeholder="00-000-XXX-XXX-000-0000.revXX",
        key="config_pattern_input",
    )

    if st.button("Parse Pattern", type="primary", disabled=not pattern.strip()):
        try:
            result = extract(pattern)
            st.session_state["parsed_standard"] = result
            st.session_state["parse_error"] = None
        except ValueError as exc:
            st.session_state["parsed_standard"] = None
            st.session_state["parse_error"] = str(exc)

    if st.session_state.get("parse_error"):
        st.error(st.session_state["parse_error"])

    # ── Parsed result ───────────────────────────────────────────────────────
    parsed = st.session_state.get("parsed_standard")
    if not parsed:
        return

    st.markdown("---")
    st.markdown("#### Parsed segments")

    rows = []
    for seg in parsed["segments"]:
        sep_display = repr(seg["separator_after"]) if seg["separator_after"] else "—"
        rows.append({
            "#":          seg["index"] + 1,
            "Placeholder": seg["placeholder"],
            "Type":       _TYPE_LABELS.get(seg["type"], seg["type"]),
            "Length":     seg["length"],
            "Separator":  sep_display,
        })
    st.table(rows)

    st.markdown("#### Generated regex")
    st.code(parsed["regex"], language="")

    st.markdown("---")
    col_save, col_clear = st.columns([1, 5])
    with col_save:
        if st.button("Confirm & Save", type="primary"):
            try:
                save_standard(parsed, CUSTOM_STANDARD_PATH)
                st.success(f"Saved to `{CUSTOM_STANDARD_PATH}`.")
                st.session_state["parsed_standard"] = None
                st.session_state["parse_error"] = None
                st.rerun()
            except OSError as exc:
                st.error(f"Could not save: {exc}")
    with col_clear:
        if st.button("Clear"):
            st.session_state["parsed_standard"] = None
            st.session_state["parse_error"] = None
            st.rerun()
