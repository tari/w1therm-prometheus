import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(name='w1therm-prometheus-exporter',
                 version='0.1.0',
                 description='1-wire temperature sensor Prometheus exporter',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 author='Peter Marheine',
                 author_email='peter@taricorp.net',
                 url='https://bitbucket.org/tari/w1therm-prometheus',
                 license='BSD2',
                 classifiers=[
                     'Environment :: No Input/Output (Daemon)',
                     'Intended Audience :: System Administrators',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: POSIX :: Linux',
                     'Programming Language :: Python :: 3 :: Only',
                     'Topic :: System :: Monitoring',
                 ],
                 py_modules='w1therm_prometheus_exporter',
                 install_requires=['w1thermsensor'],
                 entry_points={
                     'console_scripts': [
                         'w1therm-prometheus-exporter = w1therm_prometheus_exporter:console_entry_point',
                     ],
                 })
