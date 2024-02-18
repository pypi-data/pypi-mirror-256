from setuptools import setup, find_packages

VERSION = '0.2.1'

setup(
    name='nano_profiler',
    version=VERSION,
    description='Very simple profiler of time execution',
    long_description='See README.md for details',
    url='https://github.com/EvgeniyMakhmudov/nano_profiler',
    author='Makhmudov Evgeniy',
    author_email='john_16@list.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='profiler',
    packages=find_packages(),
)
