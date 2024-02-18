from setuptools import setup

setup(
    name="updog-py",
    version="0.0.1",
    packages=["updog"],
    install_requires=["psycopg2", "requests", "flask"],
)
