from setuptools import setup, find_packages

setup(
    name='allproxy',
    version='1.1.5',
    author='TheescapedShadow',
    description='Easily get a working Proxy list',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
        'packaging',
    ],
    setup_requires=['wheel'],
    include_package_data=True,
)