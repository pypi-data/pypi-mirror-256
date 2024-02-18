from setuptools import setup

setup(
    name='flask_sqlalchemy_magic_query',
    version='0.1.1',
    description='Converts HTTP URL query string parameters to flask_sqlalchemy query results',
    url='https://github.com/gabrielligoski/flask_sqlalchemy_magic_query',
    author='Gabriel Ligoski',
    author_email='gabriel.ligoski@gmail.com',
    license='MIT',
    packages=['flask_sqlalchemy_magic_query'],
    install_requires=['flask', 'sqlalchemy', 'flask_sqlalchemy']
)
