import setuptools

setuptools.setup(name='w1therm-prometheus-exporter',
                 version='0.1.0',
                 description='1-wire temperature sensor Prometheus exporter',
                 author='Peter Marheine',
                 author_email='peter@taricorp.net',
                 py_modules='w1therm_prometheus_exporter',
                 install_requires=['w1thermsensor'],
                 entry_points={
                     'console_scripts': [
                         'w1therm-prometheus-exporter = w1therm_prometheus_exporter:console_entry_point',
                     ],
                 })
