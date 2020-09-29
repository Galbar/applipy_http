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
        f'applipy@git+ssh://git@gitlab.com/Galbar2/applipy.git@{version}#&subdirectory=applipy',
        f'applipy_metrics@git+ssh://git@gitlab.com/Galbar2/applipy.git@{version}#&subdirectory=applipy_metrics',
        'aiohttp==3.6.2',
        'aiohttp_cors==0.7.0'
    ],
    scripts=[],
)
