# Python TCP/HTTP Server Coursework

An instructional IPv4 TCP server that accepts a basic HTTP request, reads a local file, and returns a minimal response. This reduced candidate contains only the server source; the client and sample HTML are withheld because their starter/source boundaries were not established.

## Server behavior

`Webserver.py` binds a socket, accepts one connection at a time, parses a simple request line, serves a path relative to its working directory, and sends basic HTTP 200 or 404 responses with content-type and content-length headers. No third-party Python packages are vendored.

## Limitations and setup

Run with `python Webserver.py <port>` in a controlled local environment. This is not for production or untrusted networks: it does not enforce a safe document-root boundary, robustly parse HTTP, validate methods, escape error-page content, or support concurrent clients. The source was not run during this review.

## Attribution and license

The source header identifies CS 3873 Program 1 and Zane. The owner confirms that they wrote essentially all substantive implementation across these four coursework projects. The archive has one copy of `Webserver.py`, matching the staged file apart from redaction of the student ID; neither it nor the related interview guide identifies a starter file or specific copied block. The assignment prompt was not present in the targeted archive folder, so no line-by-line comparison to a course scaffold is possible. Standard Python socket setup and API calls are not represented as independent original inventions. No third-party code or license marker was found. No license is included.
