from setuptools import setup, find_packages

setup(
    name='s3bids',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        's3fs',
        'boto3',
        'dask',
        'numpy',
        'pandas',
        'tqdm',
        'nibabel',
        'pybids',
        'pytest',
        # 'moto'
    ],
    # Additional metadata about your package
    description='Useful classes for downloading BIDS datasets from S3.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='pyAFQ developers',
    author_email='arokem@gmail.com',
    url='https://github.com/nrdg/s3bids',
    license='LICENSE',
)
