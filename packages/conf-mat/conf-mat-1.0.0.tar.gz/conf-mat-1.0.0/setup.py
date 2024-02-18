from setuptools import setup, find_packages

setup(
    name='conf-mat',
    version='1.0.0',
    author='khiat mohammed abderrezzak',
    author_email='khiat.abderrezzak@gmail.com',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "pandas>=2.2.0",
        "seaborn>=0.13.2",
        "pyarrow>=15.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
