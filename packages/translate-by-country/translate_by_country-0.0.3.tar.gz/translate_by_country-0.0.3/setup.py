from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()



setup(
    name='translate_by_country',  
    version= '0.0.3', 
    description='A library to translate text by country information',
    long_description='With this library, you can translate the text without choosing the language and with the characteristics of the countries',
    author='Sina157',  
    packages=find_packages(),
    author_email='sina.shams@yahoo.com', 
    url='https://github.com/Sina157/translate-by-country',  
    install_requires=[
     'googletrans==4.0.0-rc1'
    ],
    entry_points={}
)
