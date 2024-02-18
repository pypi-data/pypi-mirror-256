from setuptools import find_packages, setup

# Setup custom import schema
# cortex_cli.cli
# cortex_cli.core
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)

from general_knowledge_agent import __version__

setup(
    name="general_knowledge_agent",
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    author='Nearly Human',
    author_email='support@nearlyhuman.ai',
    description='Nearly Human General Knowledge Agent dependency for creating functional client specific agents.',
    keywords='nearlyhuman, nearly human, agent',
    # Link custom local langroid build (Fixes dependency issue with chromadb)

    python_requires='>=3.10',
    # long_description=open('README.txt').read(),
    install_requires=[
        'cortex-cli',
        'langchain==0.1.5',
        'openai==1.11.1',
        'tiktoken',
        'chromadb>=0.4.3',
        'pydantic==1.10.13',
        'openpyxl==3.1.2'
    ]
)