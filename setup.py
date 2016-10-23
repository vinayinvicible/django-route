from distutils.core import setup

from setuptools import find_packages

import django_route

try:
    with open('README.rst') as readme:
        long_description = readme.read()
except:
    long_description = ''

setup(
    name='django_route',
    version=django_route.__version__,
    packages=find_packages(),
    url='https://github.com/vinayinvicible/django-requests',
    license='MIT',
    author='Vinay Karanam',
    author_email='vinayinvicible@gmail.com',
    description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
)
