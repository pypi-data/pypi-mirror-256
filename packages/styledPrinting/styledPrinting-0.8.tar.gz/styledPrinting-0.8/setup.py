from setuptools import setup, find_packages

setup(
	name='styledPrinting',
	version='0.8',
	packages=find_packages(),
	description='A simple package to print styled text in the terminal and operate the cursor',
	author='André Ferreira',
	author_email='anfreire.dev@gmail.com',
	license='MIT',
	install_requires=[],
	python_requires='>=3.6',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)