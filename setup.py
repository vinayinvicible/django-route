from distutils.core import setup

from setuptools import find_packages

import django_route

try:
    with open('README.rst') as readme:
        long_description = readme.read()
except OSError:
    long_description = ''

setup(
    name='django_route',
    version=django_route.__version__,
    packages=find_packages(),
    url='https://github.com/vinayinvicible/django-route',
    license='MIT',
    author='Vinay Karanam',
    author_email='vinayinvicible@gmail.com',
    description='Conditional url routing for django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False,
)
