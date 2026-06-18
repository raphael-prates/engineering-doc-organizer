"""
StandardExtractor — parses and validates OTTS-016 filename segments.

Responsibilities:
- Extract individual code segments from a compliant filename
  (company code, terminal code, discipline, doc type, area, serial, revision)
- Validate each segment against the loaded standard definition
- Return structured data consumed by SuggestionEngine and the review UI
"""

import re
import json
from pathlib import Path


def extract(pattern: str) -> dict:
    """
    Parse a naming pattern like "00-000-XXX-XXX-000-0000.revXX".

    Placeholder conventions:
      0   → numeric digit
      X   → uppercase alpha character
      x   → lowercase alpha character
      rev → literal revision prefix; digits/X after it set the revision length

    Returns a dict with keys:
      pattern  – original input string
      segments – list of segment dicts (index, placeholder, type, length, separator_after)
      regex    – generated anchored regex string

    Raises ValueError on empty input or if no recognisable segments are found.
    """
    pattern = pattern.strip()
    if not pattern:
        raise ValueError("Pattern cannot be empty.")

    # re.split with a capturing group gives alternating [token, sep, token, sep, …]
    parts = re.split(r'([-._/\\|]+)', pattern)

    segments = []
    for i, part in enumerate(parts):
        if i % 2 == 1:          # separator slot — handled via separator_after on the token
            continue
        if part == '':
            continue
        seg = _infer_segment(part)
        seg["index"] = len(segments)
        seg["separator_after"] = parts[i + 1] if i + 1 < len(parts) else None
        segments.append(seg)

    if not segments:
        raise ValueError("No recognisable segments found. Use 0/X/x as placeholders.")

    # Build anchored regex
    regex_parts = [r'^']
    for seg in segments:
        regex_parts.append(_segment_to_regex(seg))
        sep = seg["separator_after"]
        if sep:
            regex_parts.append(re.escape(sep))
    regex_parts.append(r'$')

    return {
        "pattern": pattern,
        "segments": segments,
        "regex": "".join(regex_parts),
    }


def save_standard(data: dict, path: str) -> None:
    """Write a parsed standard dict to a JSON file, creating parent dirs as needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_standard(path: str) -> dict:
    """Load a standard JSON file. Returns {} if the file is absent or empty."""
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _infer_segment(token: str) -> dict:
    """Classify a placeholder token and return a partial segment dict."""
    if re.fullmatch(r'0+', token):
        return {"type": "numeric", "length": len(token), "placeholder": token}

    if re.fullmatch(r'X+', token):
        return {"type": "alpha", "case": "upper", "length": len(token), "placeholder": token}

    if re.fullmatch(r'x+', token):
        return {"type": "alpha", "case": "lower", "length": len(token), "placeholder": token}

    # revision token: literal "rev" prefix followed by digit/X placeholders
    m = re.fullmatch(r'[Rr][Ee][Vv]([0-9Xx]+)', token)
    if m:
        return {"type": "revision", "length": len(m.group(1)), "placeholder": token}

    return {"type": "alphanumeric", "length": len(token), "placeholder": token}


def _segment_to_regex(seg: dict) -> str:
    """Return the regex fragment for one segment."""
    t = seg["type"]
    n = seg["length"]
    if t == "numeric":
        return rf"\d{{{n}}}"
    if t == "alpha":
        charset = "[a-z]" if seg.get("case") == "lower" else "[A-Z]"
        return rf"{charset}{{{n}}}"
    if t == "revision":
        return r"[A-Za-z0-9]+"
    # alphanumeric fallback
    return rf"[A-Za-z0-9]{{{n}}}"
