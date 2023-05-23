import os
import sys
import time
import socket
import http.client
from urllib.parse import urlparse

# Read environment variables
check_type = os.getenv('INPUT_CHECK_TYPE')
check_timeout = int(os.getenv('INPUT_CHECK_TIMEOUT', 60))
check_http_port = os.getenv('INPUT_CHECK_HTTP_PORT', "80")
check_http_path = os.getenv('INPUT_CHECK_HTTP_PATH', "/")
check_tcp_port = os.getenv('INPUT_CHECK_TCP_PORT', "80")

ip = "localhost"


def http_request(ip, port, url_path):
    conn = http.client.HTTPConnection(ip, port=port, timeout=5)
    conn.request("GET", url_path)
    response = conn.getresponse()

    # If status is redirect (3xx), and 'location' is in headers, follow redirect
    while response.status // 100 == 3 and 'location' in response.headers:
        uri = urlparse(response.headers['location'])

        # Update host and port for redirection
        ip = uri.hostname
        port = uri.port if uri.port else 80
        url_path = uri.path

        conn = http.client.HTTPConnection(ip, port=port, timeout=5)
        conn.request("GET", url_path)
        response = conn.getresponse()

    return response


# Set the deadline
deadline = time.time() + check_timeout

# Perform different operations based on check_type
if check_type == 'HTTP':
    conn = http.client.HTTPConnection(ip, port=int(check_http_port), timeout=5)
    url = check_http_path

    while True:
        try:
            response = http_request(ip, int(check_http_port), check_http_path)
            if response.status < 200 or response.status >= 300:
                raise http.client.HTTPException(f"HTTP check failed with status {response.status}")
            print("HTTP check passed")
            break
        except Exception as e:
            print(str(e))

        if time.time() > deadline:
            print("HTTP check timeout")
            sys.exit(1)
        time.sleep(1)

elif check_type == 'TCP':
    addr = (ip, int(check_tcp_port))

    while True:
        try:
            with socket.create_connection(addr, timeout=5):
                print("TCP check passed")
                break
        except OSError as e:
            print(f"TCP check failed: {e}")

        if time.time() > deadline:
            print("TCP check timeout")
            sys.exit(1)
        time.sleep(1)

else:
    print(f"Unknown check type: {check_type}")
    sys.exit(1)
