from setuptools import setup, find_packages

setup(
    name='aori-sdk-py',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
        'websocket-client'
    ],
    author='Joshua Baker',
    author_email='joshua@aori.io',
    description='aori.io python sdk',
    keywords='aori',
    url='https://github.com/aori-io/aori-sdk-py'
)