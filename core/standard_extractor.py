"""
StandardExtractor — parses and validates OTTS-016 filename segments.

Responsibilities:
- Extract individual code segments from a compliant filename
  (company code, terminal code, discipline, doc type, area, serial, revision)
- Validate each segment against the loaded standard definition
- Return structured data consumed by SuggestionEngine and the review UI
"""
