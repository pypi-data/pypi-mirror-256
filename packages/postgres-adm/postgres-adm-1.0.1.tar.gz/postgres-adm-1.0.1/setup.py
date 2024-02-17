from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='postgres-adm',
    version='1.0.1',
    license='MIT License',
    author='Ryan Souza Anselmo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ryansouza.cwb@email.com',
    keywords='postgres-adm',
    description=u'PostgreSQL has the function of facilitating the use of methods for executing SQL statements.',
    packages=['postgres_adm'],
    install_requires=['psycopg2'],)