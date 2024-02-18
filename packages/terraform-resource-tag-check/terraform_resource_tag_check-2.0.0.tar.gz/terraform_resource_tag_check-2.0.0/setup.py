from setuptools import setup, find_packages

setup(
    name='terraform_resource_tag_check',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'checkov',
    ],
)