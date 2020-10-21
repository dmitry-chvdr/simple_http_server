#!/bin/bash

docker build . -t simple_http_server

docker run -it -d -p 8000:8000 simple_http_server