from .base import TCPServer
import os
import mimetypes


class HTTPServer(TCPServer):
    headers = {
            'Server': 'python-http-server',
            'Content-Type': 'text/html'
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'NOT Implemented'
    }

    def handle_request(self, data):
        request = HTTPRequest(data)

        try:
            handler = getattr(self, f"handle_{request.method}")
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response


    def HTTP_501_handler(self, request):

        response = HTTPResponse(status_code=501)

        # response_line = self.response_line(status_code=501)
        response_line = response.response_line()

        response_headers = response.response_headers()

        blank_line = b"\r\n"

        response_body = b"<h1>501 Not Implemented</h1>"

        return b"".join([response_line, response_headers, blank_line, response_body])


    def handle_GET(self, request):
        filename = request.uri.strip('/')

        if os.path.exists(filename):
            content_type = mimetypes.guess_type(filename)[0] or "text/html"
            extra_headers = {'Content-Type': content_type}

            response = HTTPResponse(status_code=200, extra_headers=extra_headers)

            response_line = response.response_line() 

            response_headers = response.response_headers()

            with open(filename, 'rb') as f:
                response_body = f.read()

        else:
            response = HTTPResponse(status_code=404)
            response_line = response.response_line()
            response_headers = response.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line, response_headers, blank_line, response_body])


class HTTPResponse:
    headers = {
            'Server': 'python-http-server',
            'Content-Type': 'text/html'
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'NOT Implemented'
    }

    def __init__(self, status_code, extra_headers=None):
        self.status_code = status_code
        self.extra_headers = extra_headers

    def response_line(self):
        """Returns response line"""
        reason = self.status_codes[self.status_code]
        line = f"HTTP/1.1 {self.status_code} {reason}\r\n"

        return line.encode()

    def response_headers(self):
        """Returns headers
        The `extra_headers` can be a dict for sending
        extra headers for the current response.
        """

        # make local copy of headers
        headers_copy = self.headers.copy()

        if self.extra_headers:
            headers_copy.update(self.extra_headers)

        headers = ""

        for h in headers_copy:
            headers += f"{h}: {headers_copy[h]}\r\n"

        return headers.encode()


class HTTPRequest:

    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1"

        # parse the request data
        self.parse(data)

    def parse(self, data):
        lines = data.split(b"\r\n")

        request_line = lines[0]

        words = request_line.split(b" ")

        self.method = words[0].decode() # convert bytes to str

        if len(words) > 1:
            self.uri = words[1].decode()

        if len(words) > 2:
            self.http_version = words[2]
