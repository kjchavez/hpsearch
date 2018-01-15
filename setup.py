from setuptools import setup

setup(name='hpsearch',
      version=0.1,
      description='Hyperparameter search tool',
      author='Kevin Chavez',
      author_email='kevin.j.chavez@gmail.com',
      packages=['hpsearch'],
      entry_points={ 'console_scripts': ['hpsearch = hpsearch.cli:cli'] }
     )
