from setuptools import setup, find_packages

setup(
    name='greencryptopay_py',
    version='1.0.0',
    author='greencryptopay',
    author_email='support@greencryptopay.com',
    description='This library provides convenient methods for interacting with the Greencryptopay API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GreenCryptoPay/greencryptopay_py',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ]
)