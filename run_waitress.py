#!/usr/bin/env python3

from waitress import serve
from src.pacedash.app import server as application

if __name__ == "__main__":
    serve(application, threads=100, port=8041)
