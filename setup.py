from setuptools import setup, find_packages
from os import path

# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='py_pushover_open_client',
	version='1.1.1',
	description='Unofficial Python Bindings for PushOver Open Client API',
	long_description=long_description,
    long_description_content_type="text/markdown",
	author='Jonathon Green',
	author_email='aeirsoul@gmail.com',
	url='https://github.com/Aeirsoul/py-pushover-open-client',
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3 :: Only'
	],
	
	keywords='pushover',
	
	packages=find_packages(exclude=['examples']),
	
	install_requires=['requests', 'websocket-client'],
)