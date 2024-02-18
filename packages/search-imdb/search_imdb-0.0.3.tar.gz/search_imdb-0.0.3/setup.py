from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name='search_imdb',
	version='0.0.3',
	packages=find_packages(),
	install_requires=[
	# add dependencies here.
	],
  entry_points={
    'console_scripts': [
      'search_imdb=search_imdb:hello',
      'search_imdb_test=search_imdb.__init__:hello',
    ],
  },
  long_description=long_description,
  long_description_content_type="text/markdown",
)