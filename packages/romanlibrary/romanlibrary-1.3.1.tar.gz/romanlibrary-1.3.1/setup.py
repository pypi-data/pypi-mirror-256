from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='romanlibrary',
    version='1.3.1',
    packages=find_packages(),
    install_requires=[
        #none as far as I know
    ],
    author='Cort Smith',
    author_email='cort.j.smith@gmail.com',
    description='A Python library for drawing Roman numerals using Turtle graphics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nicestuff77/roman-numeral',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='roman numeral turtle graphics drawing',
)
