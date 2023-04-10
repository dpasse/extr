import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='extr-nlp',
    version='0.0.1',
    description='',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires='',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
