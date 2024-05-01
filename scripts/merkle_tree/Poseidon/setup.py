from setuptools import setup, find_packages

setup(
    name='Poseidon',
    version='0.1.0',
    description='A Python package that runs the Poseidon hash function in Circom',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Frederico Baptista',
    author_email='',
    license='unlicensed',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: unlicensed',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    install_requires=[
        'sh',  # Utilized for running shell commands
        # Additional Python dependencies here
    ],
    python_requires='>=3.7',
    project_urls={
        'Bug Reports': '',
        'Source': '',
    },
)
