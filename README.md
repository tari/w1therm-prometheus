# Prometheus exporter for 1-wire temperature sensors

This is a simple HTTP server intended to export temperature readings from
1-wire temperature sensors like the DS18B20 in a format that can be scraped
by [Prometheus](https://prometheus.io/) for logging and monitoring.

## Requirements

This program requires Python 3 and the [`w1thermsensor`](
https://github.com/timofurrer/w1thermsensor) library, in addition to a
functional 1-wire bus (using the `w1-gpio` and `w1-therm` Linux kernel
modules). Refer to the `w1thermsensor` documentation for more information.

### Raspberry Pi

The short version of setting everything up on a Raspberry pi is as follows:

1. Add `dtoverlay=w1-gpio` to `/boot/config.txt`.
2. Connect the 1-wire data line (`DQ`) to GPIO pin 7 (GPIO4) on the Pi.
3. Connect the 1-wire Vdd and Gnd to 3.3V and Gnd on the Pi, for instance GPIO
   pins 1 and 9 respectively.
4. Reboot (for the new device tree config in step 1 to take effect).
5. Check that a sensor appears in `/sys/bus/w1/devices` and reading its
   `w1_slave` file includes 'YES' at the end of the first line.

## Installation

Install with pip. Perhaps:

```
$ pip install hg+https://bitbucket.org/tari/w1therm-prometheus#egg=w1therm-prometheus-exporter
```

## Running

Installation creates a `w1therm-prometheus-exporter` script that scans for
attached temperature sensors and starts an HTTP server which responds to all
GET requests with a response containing the current temperature of every
detected sensor.

Two command line arguments are required: the address to bind the HTTP server
to, and the port to listen on. 

Example invocation listening at localhost:9000:

```
$ w1therm-prometheus-exporter localhost 9000
```

Sample measurement capture:

```
$ curl http://localhost:9000/
# HELP w1therm_temperature Temperature in Kelvin of the sensor.
# TYPE w1therm_temperature gauge
w1therm_temperature{id="000004b926f1"} 298.15
```

## Packaging

A standalone binary can be build with [PyInstaller](
https://www.pyinstaller.org/), which may make it easier to distribute to
multiple machines. The provided `.spec` file is sufficient. For instance,
to build a standalone binary after installing with pip:

```
$ pyinstaller w1therm-prometheus-exporter.spec
```

This will output `dist/w1therm-prometheus-exporter/w1therm-prometheus-exporter`
which can be run without installation. Combining this with the provided systemd
unit file (`w1therm-prometheus-exporter.service`), the server can be run
automatically:

```
$ cp w1therm-prometheus-exporter.service /etc/systemd/system/
$ systemctl daemon-reload
$ cp dist/w1therm-prometheus-exporter /usr/local/bin/
$ systemctl start w1therm-prometheus-exporter.service
$ systemctl enable w1therm-prometheus-exporter.service
```

