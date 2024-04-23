from setuptools import setup, find_packages

setup(
    name='Poseidon',
    version='0.1.0',
    description='A Python package that interfaces with Circom',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/Poseidon',
    author='Your Name',
    author_email='your_email@example.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
        'Bug Reports': 'https://github.com/your_username/Poseidon/issues',
        'Source': 'https://github.com/your_username/Poseidon',
    },
)
