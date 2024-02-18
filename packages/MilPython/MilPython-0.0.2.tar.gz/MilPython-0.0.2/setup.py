from setuptools import setup, find_packages

setup(
    name='MilPython',
    version='0.0.2',
    description='Framework for building MILP optimizations for time series with gurobipy',
    license='MIT',
    packages=find_packages(),
    author='Hannes Hanse',
    author_email='hannes.hanse@tu-clausthal.de',
    keywords=['milp','time series','optimization','gurobi','gurobipy'],
    readme = "README.md",
    url='https://github.com/hanneshanse/MilPy',
    install_requires=["scipy","gurobipy","numpy","matplotlib"],
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
)