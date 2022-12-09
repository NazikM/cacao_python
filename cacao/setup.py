from setuptools import setup, find_packages


setup(
    name='multi-cacao',
    version='0.6',
    license='MIT',
    author="Nazarii Marusyn",
    author_email='marusinnazar@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/NazikM/cacao_python',
    keywords='cacao',
)
