from setuptools import setup, find_packages

setup(
    name='rosepyt',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'Flask',
        'discord.py',
        'py-cord',
        'SQLAlchemy',
        'httpx',
        'uvicorn',
        'pydantic',
        'gino'
    ],
)