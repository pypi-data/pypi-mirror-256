from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name='letterboxdpy_test',
	version='1.0.1',
	packages=find_packages(),
	install_requires=[
	# add dependencies here.
	],
  entry_points={
    'console_scripts': [
    ],
  },
  long_description=long_description,
  long_description_content_type="text/markdown",
)