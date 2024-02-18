from setuptools import setup, find_packages

setup(
    name='check_terraform_resource_tags',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'checkov',
    ],
)