
from setuptools import setup, find_packages

setup(
    name='rediscollectiondb',
    version='0.1.0',
    author='Guruh Purnama',
    author_email='guruh@xgn.ai',
    description='A simple interface to manage collections in Redis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'redis',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
