import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='extr',
    version='0.0.2',
    description='Named Entity Recognition (NER) and Relation Extraction (RE) library using Regular Expressions',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires='',
    long_description=long_description,
    long_description_content_type='text/markdown',
)