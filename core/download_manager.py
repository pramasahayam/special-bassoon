import os
import requests
from skyfield.api import Loader

class DownloadManager:
    def __init__(self, base_folder='ephemeris_data'):
        self.base_folder = base_folder
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
        self.loader = Loader(self.base_folder)
        
        # Ephemeris Data URLs
        self.ephemeris_urls = [
            'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp',
            'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/jup365.bsp',
            'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/mar097.bsp',
            'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/ura111l.bsp'
        ]

    def download_with_progress(self, url, file_path):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=8192):
                file.write(data)
                downloaded_size += len(data)
                self.progress = downloaded_size / total_size  # Progress tracking

    def load(self, data_url):
        file_name = data_url.split('/')[-1]
        file_path = os.path.join(self.base_folder, file_name)

        if not os.path.isfile(file_path):
            try:
                self.download_with_progress(data_url, file_path)
            except Exception as e:
                print(f"Error downloading with progress: {e}. Falling back to Skyfield Loader.")
                self.loader.download(data_url)

        return file_path

    def pre_download_all(self):
        for url in self.ephemeris_urls:
            self.load(url)
