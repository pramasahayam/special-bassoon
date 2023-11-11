import os
import requests
import threading
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

        self.file_progress = {url: 0 for url in self.ephemeris_urls}

    def download_with_progress(self, url, file_path):
        """
        Custom method to download a file with progress tracking.
        """
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=8192):
                file.write(data)
                downloaded_size += len(data)
                self.file_progress[url] = downloaded_size / total_size  # Update progress

    def load(self, data_url):
        file_name = data_url.split('/')[-1]
        file_path = os.path.join(self.base_folder, file_name)

        if os.path.isfile(file_path):
            # If the file already exists, mark its download as complete
            self.file_progress[data_url] = 1.0
        else:
            try:
                self.download_with_progress(data_url, file_path)
            except Exception as e:
                print(f"Error downloading with progress: {e}. Falling back to Skyfield Loader.")
                self.loader.download(data_url)
                self.file_progress[data_url] = 1.0

        return file_path

    def pre_download_all(self):
        """
        Method to pre-download all ephemeris data.
        """
        for url in self.ephemeris_urls:
            self.load(url)

    def pre_download_all_async(self):
        """
        Start asynchronous pre-download of all ephemeris data.
        """
        download_thread = threading.Thread(target=self.pre_download_all)
        download_thread.start()

    def get_download_progress(self):
        """
        Method to get the current download progress.
        """
        total_progress = sum(self.file_progress.values())
        return total_progress / len(self.ephemeris_urls) if self.ephemeris_urls else 1.0

    def is_download_complete(self):
        """
        Check if all downloads are complete.
        """
        return all(progress == 1.0 for progress in self.file_progress.values())

