__author__="hari"
__date__ ="$Aug 9, 2009 5:49:02 PM$"

from distutils.core import setup
setup (
  name = 'gridder',
  version = '0.5',
  package_dir={'gridder': 'src'},
  packages=['gridder'],

  # Declare your packages' dependencies here, for eg:
  install_requires=['reportlab','pyyaml'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'hari jayaram',
  author_email = 'harijay@gmail.com',
  url = 'http://www.code-itch.com/gridzilla',
  license = 'MIT licence',
  long_description= 'gridder(protein-crystallization-gridmaker) the classes behing GridZilla',

  # could also include long_description, download_url, classifiers, etc.

  
)
