from setuptools import setup

with open('README.md') as f:
    longdesc = f.read()

version = '3.5.0'

config = {
    'description': 'Tax Calculator',
    'url': 'https://github.com/PSLmodels/Tax-Calculator',
    'download_url': 'https://github.com/PSLmodels/Tax-Calculator',
    'description': 'taxcalc',
    'long_description': longdesc,
    'version': version,
    'license': 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'packages': ['taxcalc', 'taxcalc.cli'],
    'include_package_data': True,
    'name': 'taxcalc',
    'install_requires': ['setuptools', 'numpy', 'pandas', 'bokeh', 'numba'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    'tests_require': ['pytest'],
    'entry_points': {
        'console_scripts': ['tc=taxcalc.cli.tc:cli_tc_main']
    }
}

setup(**config)
