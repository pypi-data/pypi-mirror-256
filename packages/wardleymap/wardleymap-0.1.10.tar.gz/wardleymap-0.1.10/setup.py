from setuptools import setup, find_packages

setup(
    name='wardleymap',
    version='0.1.10',
    author='Mark Craddock',
    author_email='python@firstliot.uk',
    description='A Python package to create and visualize Wardley Maps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://wardleymaps.ai/',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'streamlit',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
