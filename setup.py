from setuptools import setup, find_packages

setup(
	name='py-pushover-open-client',
	version='1.0.0a1',
	description='Unofficial Python Bindings for PushOver Open Client API',
	author='Jonathon Green',
	author_email='',
	url='https://github.com/Aeirsoul/py-pushover-open-client',
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		
		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5'
	],
	
	keywords='',
	
	packages=find_packages(exclude=['docs', 'tests*']),
	
	install_requires=['requests', 'websocket-client'],
)