# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.realpath(__file__))
readme = os.path.join(here, 'README.rst')

setup(
    name='chivato',
    version='0.0.1',
    description='VAT identification number validator',
    long_description=open(readme).read(),
    author='Javier Santacruz',
    author_email='javier.santacruz.lc@gmail.com',
    url='http://github.com/jvrsantacruz/chivato',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    platforms=['Any'],
)
