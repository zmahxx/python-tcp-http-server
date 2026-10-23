# Name: Zane Mullinax
# Course: CS 3873 - Program 1

from socket import *
import sys
import os

RECV_SIZE = 2048

def get_content_type(name: str) -> str:
    if name.endswith((".html", ".htm")):
        return "text/html"
    if name.endswith(".txt"):
        return "text/plain"
    return "application/octet-stream"

def send_response(sock, status_line: str, content_type: str, body: bytes) -> None:
    header = (
        f"{status_line}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()
    sock.sendall(header + body)

def make_404_body(path: str) -> bytes:
    # Small HTML response
    safe = path if path else ""
    return f"<html><body><h1>404 Not Found</h1><p>{safe}</p></body></html>".encode()

if len(sys.argv) != 2:
    print("Usage: python3 Webserver.py serverPort")
    sys.exit(1)

serverPort = int(sys.argv[1])

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

try:
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print(f"Server is listening on port: {serverPort}")

    while True:
        print("Ready to receive...")

        connectionSocket, addr = serverSocket.accept()
        with connectionSocket:
            try:
                req_bytes = connectionSocket.recv(RECV_SIZE)
                if not req_bytes:
                    continue

                req_text = req_bytes.decode(errors="replace")
                first_line = req_text.splitlines()[0] if req_text else ""
                print(f"Client {addr} sent:\n{req_text}")

                parts = first_line.split()
                if len(parts) < 2:
                    continue

                # "GET /HelloWorld.html HTTP/1.1" -> "HelloWorld.html"
                path = parts[1]
                if path.startswith("/"):
                    path = path[1:]

                if not path:
                    continue

                # Stop rule: "stop" base name, any extension, file must NOT exist
                base = os.path.splitext(path)[0].lower()
                if base == "stop" and not os.path.isfile(path):
                    print("Stop request received. Shutting down server.")

                    break

                if not os.path.isfile(path):
                    body = make_404_body(path)
                    send_response(connectionSocket, "HTTP/1.1 404 Not Found", "text/html", body)
                    continue

                with open(path, "rb") as f:
                    body = f.read()

                ctype = get_content_type(path)
                send_response(connectionSocket, "HTTP/1.1 200 OK", ctype, body)

            except Exception as e:
                # Keep server running even if one request is weird
                print(f"Request error: {e}")

except KeyboardInterrupt:
    print("\nInterrupt received (Ctrl+C). Closing server.")
finally:
    try:
        serverSocket.close()
    except Exception:
        pass
    sys.exit(0)
