from setuptools import setup

setup(
    name='pypgwrapper',
    version='1.0.0',
    description='Python wrapper for Postgres',
    author = 'Abel Tavares',
    url = 'https://github.com/abeltavares/pypostgres',
    author_email = 'abelst9@gmail.com',
    packages=['pypgwrapper'],
    install_requires=[
        'psycopg2',
        'tabulate'
    ],
    license = 'BSD',
    classifiers = [ "Topic :: Database",
                      "Programming Language :: Python :: 3",
                ]
)