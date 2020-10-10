import typing as T

from setuptools import setup, find_packages
from distutils.util import convert_path

ns: T.Dict[str, str] = {}
ver_path = convert_path('applipy_web/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), ns)
version = ns['__version__']


setup(
    name='applipy_web',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Library for building web services using applipy',
    license='Apache 2.0',
    author='Alessio Linares',
    author_email='mail@alessio.cc',
    version=version,
    packages=find_packages(exclude=['doc', 'tests']),
    data_files=[],
    python_requires='>=3.6',
    install_requires=[
        'applipy==0.12',
        'applipy_metrics==0.11',
        'aiohttp==3.6.2',
        'aiohttp_cors==0.7.0',
    ],
    scripts=[],
)
