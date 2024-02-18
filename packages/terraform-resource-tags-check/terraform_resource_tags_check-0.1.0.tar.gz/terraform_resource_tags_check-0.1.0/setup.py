from setuptools import setup, find_packages

setup(
    name='terraform_resource_tags_check',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'checkov',
    ],
)