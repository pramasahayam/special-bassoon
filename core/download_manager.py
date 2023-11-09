import os
from skyfield.api import Loader

class DownloadManager:
    def __init__(self, base_folder='ephemeris_data'):
        self.base_folder = base_folder
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
        self.loader = Loader(self.base_folder)

    def load(self, data_url):
        # Extract file name from URL
        file_name = data_url.split('/')[-1]
        file_path = os.path.join(self.base_folder, file_name)
        
        # Check if the file already exists
        if not os.path.isfile(file_path):
            # Download the file
            print(f"Downloading ephemeris data to {file_path}")
            self.loader.download(data_url)
        
        return file_path
