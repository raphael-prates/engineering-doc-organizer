"""
SuggestionEngine — builds rename proposals for non-standard files.

Responsibilities:
- Accept a list of EngineeringFile objects (pattern == "unknown" or "trash")
- Infer the correct OTTS-016 compliant filename using available metadata
- Return a ranked list of SuggestionResult objects for user review
- Delegate standard-code extraction to StandardExtractor
"""
