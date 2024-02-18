from setuptools import setup

setup(
    name='gwss',
    version='0.0.1',

    url='',
    scripts=['bin/gwss'],
    license='MIT',
    author='Ken Spencer / IotaSpencer',
    author_email='me@iotaspencer.me',
    description='get web scripts & styles',
    long_description='get web scripts and styles',
    packages=['gwss'],
    install_requires=[
        'lastversion~=3.4.6',
        'aiohttp~=3.9.2',
        'click~=8.1.7',
        'pytest~=8.0.0',
        'setuptools~=59.6.0'
    ],
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Typing :: Typed",
        "Topic :: System :: Software Distribution"
    ]
)
