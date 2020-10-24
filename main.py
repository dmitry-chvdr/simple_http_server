import os
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


class SimpleHandler(BaseHTTPRequestHandler):

    BASE_DIR = 'store/'
    MAX_FILE_SIZE = 2 ** 38

    def _build_file_path(self, file_name):
        try:
            os.mkdir(f'{self.BASE_DIR}{file_name[:2]}')
        except FileExistsError:
            pass
        finally:
            file_path = f'{self.BASE_DIR}{file_name[:2]}/{file_name}'
        return file_path

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

    def _read_by_chunks(self, fd, chunk_size=2**15, size=MAX_FILE_SIZE):
        while True:
            current_chunk_size = min(chunk_size, size)
            if current_chunk_size <= 0:
                return

            chunk = fd.read(current_chunk_size)
            size -= chunk_size
            if not chunk:
                return
            yield chunk

    def close_header_multipart(self):
        self.send_header('content-type', 'multipart/form-data')
        self.end_headers()

    def close_header_text(self):
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        file_path = self._get_file_path()
        try:
            self.send_response(200)
            self.close_header_multipart()
            with open(file_path, 'rb') as fd:
                for chunk in self._read_by_chunks(fd):
                    self.wfile.write(chunk)
        except (FileNotFoundError, IsADirectoryError):
            file_name = self._get_file_name()
            self.send_response(404, f'File with hash = {file_name} not found')
            self.close_header_multipart()

    def do_POST(self):
        try:
            http_body_size = int(self.headers.get('content-length'), 0)
            chunked_data_generator = self._read_by_chunks(self.rfile,
                                                          size=http_body_size)

            tmp_src = "tmp_file"
            m = hashlib.sha1()
            with open(tmp_src, "wb") as file:
                for chunk in chunked_data_generator:
                    m.update(chunk)
                    file.write(chunk)

            file_name = m.hexdigest()
            file_path = self._build_file_path(file_name)
            os.rename(tmp_src, file_path)

            self.send_response(201)
            self.close_header_text()
            self.wfile.write(file_name.encode())
        except Exception as e:
            print(e)
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