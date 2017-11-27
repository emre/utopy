from setuptools import setup

setup(
    name='utopy',
    version='0.0.1',
    py_modules=['utopy'],
    url='http://github.com/emre/utopy',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
        description='Utopian curation bot',
    entry_points={
        'console_scripts': [
            'utopy = utopy:main',
        ],
    },
    install_requires=['steem', 'dataset', 'requests']
)