from setuptools import setup, find_packages

setup(
	name='search_imdb',
	version='0.0.1',
	packages=find_packages(),
	install_requires=[
	# add dependencies here.
	],
  entry_points={
    'console_scripts': [
      'search_imdb=search_imdb:hello',
      'search_imdb_test=search_imdb.__init__:hello',
    ],}
)