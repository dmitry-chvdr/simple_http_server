import os
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


class SimpleHandler(BaseHTTPRequestHandler):

    BASE_DIR = 'store/'

    def _make_file_name(self, data):
        file_name = hashlib.sha1(data).hexdigest()
        return file_name

    def _build_file_path(self, data):
        file_name = self._make_file_name(data)
        try:
            os.mkdir(f'{self.BASE_DIR}{file_name[:2]}')
        except FileExistsError:
            pass
        finally:
            file_path = f'{self.BASE_DIR}{file_name[:2]}/{file_name}'
        return file_path, file_name

    def _get_file_name(self):
        file_name = self.path[6:]
        return file_name

    def _get_file_path(self):
        file_name = self._get_file_name()
        file_path = f'{self.BASE_DIR}{file_name[:2]}/{file_name}'
        return file_path

    def _delete_file(self):
        file_path = self._get_file_path()
        file_name = self._get_file_name()
        os.remove(file_path)
        try:
            os.rmdir(f'{self.BASE_DIR}{file_name[:2]}')
        except OSError:
            pass

    def close_header_multipart(self):
        self.send_header('content-type', 'multipart/form-data')
        self.end_headers()

    def close_header_text(self):
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        file_path = self._get_file_path()
        try:
            file = open(file_path, 'rb')
            self.send_response(200)
            self.close_header_multipart()
            self.wfile.write(file.read())
            file.close()
        except (FileNotFoundError, IsADirectoryError):
            file_name = self._get_file_name()
            self.send_response(404, f'File with hash = {file_name} not found')
            self.close_header_multipart()

    def do_POST(self):
        data = self.rfile.read(int(self.headers.get('content-length')))
        file_path, file_name = self._build_file_path(data)
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
            self.send_response(201)
            self.close_header_text()
            self.wfile.write(file_name.encode())
        except:
            self.send_response(500)
            self.close_header_text()

    def do_DELETE(self):
        try:
            self._delete_file()
            self.send_response(204)
        except FileNotFoundError:
            self.send_response(404, 'File not found')
        finally:
            self.close_header_text()


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


PORT = 8000
Handler = SimpleHandler


with ThreadingSimpleServer(('0.0.0.0', PORT), Handler) as httpd:
    httpd.serve_forever()
