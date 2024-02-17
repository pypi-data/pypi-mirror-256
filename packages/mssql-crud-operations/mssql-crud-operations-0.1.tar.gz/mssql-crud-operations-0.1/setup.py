from setuptools import setup, find_packages

setup(
    name='mssql-crud-operations',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyodbc',
        'python-dotenv',
    ],
)
