import json
import re
import os
from config.settings import OTTS016_PATTERN, OTTS016_NO_REVISION
from core.models import EngineeringFile

class Classifier:
    def __init__(self):
        # Load OTTS-016 standard once when object is created
        with open('config/standards/otts016.json', 'r') as f:
            self.standard = json.load(f)

    def classify(self, files):
        # Receive list of EngineeringFile objects from Scanner
        for file in files:
            # Process each file according to its detected pattern
            if file.pattern == "standard":
                # Remove extension to get clean name for regex
                name = os.path.splitext(file.filename)[0]
                match = re.match(OTTS016_PATTERN, name)
                if match:
                    # Assign captured groups to file attributes
                    file.company_code    = match.group(1)
                    file.terminal_code   = match.group(2)
                    file.discipline_code = match.group(3)
                    file.doc_type        = match.group(4)
                    file.area_code       = match.group(5)
                    file.serial_number   = match.group(6)
                    file.revision        = match.group(7)

                    # Validate codes against OTTS-016 standard
                    if file.discipline_code not in self.standard['discipline_codes']:
                        file.flags.append('invalid_discipline')
                    if file.doc_type not in self.standard['document_type_codes']:
                        file.flags.append('invalid_doc_type')
                    if file.area_code not in self.standard['area_codes']:
                        file.flags.append('unknown_area_code')
                else:
                    # Try without revision
                    match = re.match(OTTS016_NO_REVISION, name)
                    if match:
                        file.company_code    = match.group(1)
                        file.terminal_code   = match.group(2)
                        file.discipline_code = match.group(3)
                        file.doc_type        = match.group(4)
                        file.area_code       = match.group(5)
                        file.serial_number   = match.group(6)
                        file.revision        = None
                        # Flag — revision missing
                        file.flags.append('missing_revision')

                # Set status and suggested name
                file.status = "active"
                file.suggested_name = file.filename

            elif file.pattern == "unknown":
                # Flag for AI classification (Sprint 5)
                file.flags.append('needs_ai_classification')
                file.suggested_name = None

            elif file.pattern == "trash":
                # Add flag and set status
                file.flags.append('trash')
                file.status = "trash"

        # Detect orphan DWGs before returning
        self.find_orphan_dwgs(files)

        # Return enriched list of EngineeringFile objects
        return files

    def find_orphan_dwgs(self, files):
    # Build a set of all PDF filenames without extension for global lookup
        pdf_names = set()
        for file in files:
            if file.extension.lower() == '.pdf':
                # store only filename without extension
                name_without_ext = os.path.splitext(file.filename)[0]
                pdf_names.add(name_without_ext)

        # Check each DWG against the global PDF set
        for file in files:
            if file.extension.lower() == '.dwg':
                name_without_ext = os.path.splitext(file.filename)[0]
                if name_without_ext not in pdf_names:
                    file.flags.append('orphan_dwg')

    def validate_move(self, file, destination):
        # Raise SecurityError if destination is outside project_root
        if not destination.startswith(file.project_root):
            raise ValueError(f"Move blocked: {file.filename} cannot leave {file.project_root}")