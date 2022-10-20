from server import HTTPServer

if __name__ == '__main__':
    try:
        server = HTTPServer()
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down")
        exit()

