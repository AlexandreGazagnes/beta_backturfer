#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages

install_requires = [    'pandas',
                        'numpy',
                        'matplotlib', 
                        'seaborn',
                        'tqdm',
                        'flask',
                        'flask_session',
                        'flask_wtf', 
                        'wtforms',
                        'bs4',     ]


setup(  name            = 'beta_backturfer',
        version         = '0.1',
        packages        = find_packages(),
        author          = 'Alexandre Gazagnes',
        author_email    = 'a.gazagnes@gmail.com',
        description     = 'An easy to use library to try various back turfing strats',
        long_description= open('README.md').read(),
        url             = 'https://github.com/AlexandreGazagnes/beta_backturfer',
        install_requires= install_requires,
        license         = 'GNU'     )

