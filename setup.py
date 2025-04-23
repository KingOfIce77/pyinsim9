#!/usr/bin/env python

import os
from distutils.core import setup

example_files = [os.path.join('examples', p) for p in os.listdir('examples') if not p.startswith('_')]
doc_files = ['COPYING', 'COPYING.LESSER', 'README.md', 'VERSION']

setup(name='pyinsim9',
      version='3.1.0',
      description='InSim library for the Python programming language',
      author='Remi Arnaud',
      author_email='kingofice.lfs@gmail.com',
      url='https://github.com/KingOfIce77/pyinsim9',
      packages=['pyinsim9'],
      data_files=[('docs', doc_files),
                  ('examples', example_files)])
