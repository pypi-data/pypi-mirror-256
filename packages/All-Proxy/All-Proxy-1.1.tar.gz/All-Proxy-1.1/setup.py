from setuptools import setup, find_packages

setup(
    name='All-Proxy',
    version='1.1',
    author='TheescapedShadow',
    description='Easily get a working Proxy list',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
    ],
)