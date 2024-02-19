from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name='FinRecipes',
    version='0.0.4',
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

    long_description=description,
    long_description_content_type='text/markdown'
)