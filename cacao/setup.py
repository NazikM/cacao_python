from setuptools import setup, find_packages


setup(
    name='multi-cacao',
    version='1.0',
    license='MIT',
    author="Nazarii Marusyn",
    author_email='marusinnazar@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/NazikM/cacao_python/tree/master/cacao',
    keywords='cacao',
)
