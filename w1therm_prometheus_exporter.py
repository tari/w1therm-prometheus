#!/usr/bin/env python3

import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from w1thermsensor import W1ThermSensor

SENSORS = W1ThermSensor.get_available_sensors()

class Exporter(BaseHTTPRequestHandler):
    METRIC_HEADER = ('# HELP w1therm_temperature Temperature in Kelvin of the sensor.\n'
                     '# TYPE w1therm_temperature gauge\n')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_sensor_states(self):
        return {
            sensor.id: sensor.get_temperature('kelvin')
            for sensor in SENSORS
        }

    def build_exposition(self, sensor_states):
        out = self.METRIC_HEADER
        for sensor, temperature in sensor_states.items():
            out += 'w1therm_temperature{{id="{}"}} {}\n'.format(sensor, temperature)
        return out

    def do_GET(self):
        response = self.build_exposition(self.get_sensor_states())
        response = response.encode('utf-8')

        # We're careful to send a content-length, so keepalive is allowed.
        self.protocol_version = 'HTTP/1.1'
        self.close_connection = False

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Backport of http.server.ThreadingHTTPServer from Python 3.7."""
    daemon_threads = True


def main(argv, stderr):
    if len(argv) != 3:
        print("Missing required bind address and port", file=stderr)
        print("Sample usage:", argv[0], "localhost 8080", file=stderr)
        return 1
    (addr, port) = argv[1:]
    port = int(port)

    print('Starting HTTP server at {}:{}'.format(addr, port))
    server = ThreadingHTTPServer((addr, port), Exporter)
    server.serve_forever()


def console_entry_point():
    import sys
    sys.exit(main(sys.argv, sys.stderr))


if __name__ == '__main__':
    console_entry_point()
