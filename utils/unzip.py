import base64
import zipfile
import io


class UnZip:
    def __init__(self, content):
        decoded_data = base64.b64decode(content)
        self.zip_data = io.BytesIO(decoded_data)

    def get_filelist(self):
        with zipfile.ZipFile(self.zip_data, 'r') as zip_file:
            return zip_file.namelist()

    def retrieve(self, filename):
        with zipfile.ZipFile(self.zip_data, 'r') as zip_file:
            with zip_file.open(filename) as file:
                file_content = file.read()
                return file_content.decode('utf-8', errors='ignore')
