from setuptools import setup, find_packages

install_requires = [
    'pandas',
    'pyarrow >= 0.12.1',
    'tqdm >= 4.31.1',
]

setup(
    name='beta_backturfer',
    version='0.1',
    packages=find_packages(),
    author='Alexandre Gazagnes',
    author_email='a.gazagnes@gmail.com',
    description='An easy to use library to try various back turfing strats',
    long_description=open('README.md').read(),
    url='https://github.com/alexandregazagnes/beta_backturfer',
    install_requires=install_requires,
    license='GNU',
)

