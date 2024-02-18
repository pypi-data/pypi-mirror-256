from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name = 'cedisa_report',
    version = '1.5.0',
    author = 'Gustavo Gomes Dias',
    author_email = 'gustavo.dias@cedisa.com.br',
    packages = ['cedisa_report'],
    description=readme
)