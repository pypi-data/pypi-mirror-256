from setuptools import setup, find_packages

setup(
    name='Radisys90',
    version='1.0.1',
    description='marionette',
    long_description='marionette_driver',
    license='MIT',
    packages=find_packages(),
    author='shayan',
    author_email='syedshayan109@gmail.com',
    install_requires=['mozrunner==8.3.0',
                      'mozversion==2.4.0',
                      'six==1.16.0',
                      'future==0.18.3',
                      'manifestparser==2.1.0'],
    keywords=['radisys90', 'r90'],
    download_url='https://pypi.org/project/radisys90/'
)

