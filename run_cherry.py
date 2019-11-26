#!/usr/bin/env python3

from cheroot import wsgi
from src.pacedash.app import server as application

###used to run the dashboard on a windows server instance
### uses cheroot to open the dashboard on port 8041
if __name__ == "__main__":
    server = wsgi.Server(
        ("0.0.0.0", 8041),
        application,
        numthreads=250,
        server_name="internal.pace.dashboard",
        request_queue_size=50,
    )
    try:
        print("Server started")
        server.start()
    except KeyboardInterrupt:
        print("Server stopped")
        server.stop()
