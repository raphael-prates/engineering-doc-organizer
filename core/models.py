class EngineeringFile:

    def __init__(self, path, filename, extension, size, date, path_length, project_root):
    # Known at scan time
        self.path = path
        self.filename = filename
        self.extension = extension
        self.size = size
        self.date = date
        self.path_length = path_length
        self.project_root = project_root  # boundary — file never leaves this folder

    # Filled by Classifier
        self.suggested_name = None
        self.title = None
        self.discipline_code = None
        self.doc_type = None
        self.serial_number = None
        self.revision = None
        self.status = None
        self.flags = []
        self.pattern = None  # standard / unknown / trash

class Project:

    def __init__(self, name, year, folder_path):
        self.name = name
        self.year = year
        self.folder_path = folder_path
        self.files = [] # Starts empty, Scanner will populate
