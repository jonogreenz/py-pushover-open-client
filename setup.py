from setuptools import setup, find_packages

setup(
	name='py_pushover_open_client',
	version='1.0.1',
	description='Unofficial Python Bindings for PushOver Open Client API',
	author='Jonathon Green',
	author_email='',
	url='https://github.com/Aeirsoul/py-pushover-open-client',
	license='MIT',
	classifiers=[
		'Development Status :: 4 - Beta',

		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		
		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 3.0'
		'Programming Language :: Python :: 3.1'
		'Programming Language :: Python :: 3.2'
		'Programming Language :: Python :: 3.3'
		'Programming Language :: Python :: 3.4'
		'Programming Language :: Python :: 3.5'
	],
	
	keywords='',
	
	packages=find_packages(exclude=['docs', 'tests*']),
	
	install_requires=['requests', 'websocket-client'],
)