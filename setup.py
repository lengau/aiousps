import codecs
import os
import re
from setuptools import find_packages, setup


setup(
    name='aiousps',
    version='0.1',
    author='Alex Lowe',
    author_email='amlowe@lengau.net',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/lengau/usps-api',
    license='MIT',
    description='Python wrapper for the USPS API',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords='usps shipping',
    long_description=open('README.rst', 'r').read(),
    install_requires=['requests', 'lxml', 'xmltodict'],
    extras_require={
        ':python_version == "3.6"': ['dataclasses']
    },
    tests_require=['coverage', 'hypothesis', 'pytest', 'pytest-cov', 'pytest-asyncio'],
    zip_safe=False,
)