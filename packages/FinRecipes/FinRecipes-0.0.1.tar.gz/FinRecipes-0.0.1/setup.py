from setuptools import setup, find_packages

setup(
    name='FinRecipes',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[ 
        # Add dependencies here.
        'pandas',
        'progressbar',
        'yfinance',
        'stockstats',
        'datetime',
        'pytz',
        'numpy',
        'tables'
    ],
)