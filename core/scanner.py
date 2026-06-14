
import os
import csv
import re
from core.models import EngineeringFile, Project
from config.settings import TRASH_PREFIXES, TRASH_FILENAMES, OTTS016_PATTERN, MAX_PATH_LENGTH

# Scan chosen folder recursively and collect all file information
# Export results to CSV file for further processing

class Scanner:
    def scan(self, root_path, is_new_project = False):
        # False → Cleanup | True → Onboarding
        files = []
        for folder, subfolders, filenames in os.walk(root_path):
            for filename in filenames:
                # 1. Build full file path by joining folder and filename
                full_path = os.path.join(folder, filename)

                # 2. Extract file metadata from the filesystem
                extension = os.path.splitext(filename)[1]
                size = os.path.getsize(full_path)
                date = os.path.getmtime(full_path)
                path_length = len(full_path)

                # 3. Create EngineeringFile object with collected metadata
                file = EngineeringFile(full_path, filename, extension, size, date, path_length, root_path)
                file.pattern = self.detect_pattern(filename) # Detect and assign naming pattern (Standard / Unknown / Trash)
                if not self.check_path_length(full_path): # Check if full path exceeds Windows MAX_PATH limit (260 chars) If path is too long, add warning flag to the file
                    file.flags.append('path_too_long')

                # 4. Append file object to the results list
                files.append(file)       
        return files

    def export_csv(self, files, output_path):
        # Open output file in write mode with UTF-8 encoding for special characters
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header row with column names
            writer.writerow(['filename', 'extension', 'size', 'date', 'path_length', 'project_root', 'pattern'])
            # Write one row per EngineeringFile object
            for f in files:
                writer.writerow([f.filename, f.extension, f.size, f.date, f.path_length, f.project_root, f.pattern])
    
    def detect_pattern(self, filename):   
        name = os.path.splitext(filename)[0]
        # Remove file extension to check only the name
        if re.match(OTTS016_PATTERN, name):
            # Match against OTTS-016 regex pattern from settings
            # If match → return "Standard"
            # If filename starts with known trash prefix or is a known trash file → return "Trash"
            # Otherwise → return "Unknown"
            return "Standard"
        elif any(filename.startswith(p) for p in TRASH_PREFIXES) or filename in TRASH_FILENAMES:
            return "Trash"
        else:
            return "Unknown"

    def check_path_length(self, path):
        # Return True if path length is within Windows limit
        # Return False if path length exceeds MAX_PATH_LENGTH (260 chars)
        return len(path) <= MAX_PATH_LENGTH
    


