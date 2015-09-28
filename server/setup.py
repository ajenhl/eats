#!/usr/bin/env python3

from setuptools import find_packages, setup


setup(
    name = 'eats',
    version = '1.0.0',
    description = 'Django app for recording, editing, using and displaying authority information about entities.',
    long_description = 'EATS (the Entity Authority Tool Set) is a web application for recording, editing, using and displaying authority information about entities. It is designed to allow for multiple authorities to each maintain their own independent data, while operating on a common base that means information about the same entity is all in one place.',
    url = 'https://github.com/ajenhl/eats',
    author = 'Jamie Norrish',
    author_email = 'jamie@artefact.org.nz',
    license = 'GNU General Public License v3',
    packages = find_packages(),
    install_requires = ['Django>=1.8', 'lxml', 'django_tmapi',
                        'django-selectable'],
    classifiers = [
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
