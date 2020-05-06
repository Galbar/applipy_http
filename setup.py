from setuptools import setup, find_packages

try:
    from applipy_web import Version
except ImportError as e:
    # ImportError will happen if any dependency is missing
    Version = e.args[-1]


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
    dependency_links=['git+ssh://git@gitlab.com/Galbar2/applipy.git#egg=applipy&subdirectory=applipy',
                      'git+ssh://git@gitlab.com/Galbar2/applipy.git#egg=applipy_metrics&subdirectory=applipy_metrics'],
    install_requires=['aiohttp==3.2.1',
                      'aiohttp_cors==0.7.0'],
    scripts=[],
)
