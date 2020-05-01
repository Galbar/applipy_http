from setuptools import setup, find_packages
from applipy_web import Version

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
    version=Version.RELEASE,
    packages=find_packages(exclude=['doc', 'tests']),
    data_files=[],
    python_requires='~=3.6',
    install_requires=['applipy',
                      'applipy_metrics',
                      'aiohttp==3.2.1',
                      'aiohttp_cors==0.7.0'],
    scripts=[],
)
