from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()



setup(
    name='translate_by_country',  # The name of the package
    version= '0.0.1',  # the version number of the package
    description='A module to translate with country information',
    # A short description of package
    long_description=readme,
    # A long description of package
    author='Sina157',  # The maintainer
     packages=find_packages(),
    author_email='sina.shams@yahoo.com',  # The maintainer's email address
    url='https://github.com/Sina157/translate-by-country',  # The package's website
    install_requires=[
     'googletrans==4.0.0-rc1'
    ],
    entry_points={}
)
