from setuptools import setup, find_packages

setup(
    name='nfs_creator',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'distro==1.9.0'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)

# command to build the python dist: python setup.py sdist bdist_wheel
# command to install the package: pip install dist/nfs_creator-0.1-py3-none-any.whl