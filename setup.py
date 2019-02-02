#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='django-unifi-portal',
    version='0.0.2',
    author='bsab',
    author_email='tino.saba@gmail.com',
    url='https://github.com/bsab/django-unifi-portal',
    description='Authenticate Unifi WiFi Guests with Django.',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django>=1.10,<=1.11",
        "django-braces==1.13",
        "requests==2.21",
        "django-material==1.4.3",
        "requests-toolbelt==0.8.0",
        "Pillow==5.4.1",
    ],
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)