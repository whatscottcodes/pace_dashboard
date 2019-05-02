#!/usr/bin/env python3

from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
from src.pacedash.app import server as application

if __name__ == "__main__":
    server = wsgi.Server(("0.0.0.0", 8041), application, numthreads = 250, server_name="internal.pace.dashboard", request_queue_size=50)
    #server.ssl_adapter = BuiltinSSLAdapter(certificate = "E:\\SSL\\openssl.crt",
    #    private_key = "E:\\SSL\\openssl.key")
    try:
        print('Server started')
        server.start() 
    except KeyboardInterrupt:
        print('Server stopped')
        server.stop()
