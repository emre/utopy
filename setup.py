from setuptools import setup

setup(
    name='utopy',
    version='0.0.9',
    packages=["utopy",],
    url='http://github.com/emre/utopy',
    license='MIT',
    author='emre yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Curation bot for steem network',
    entry_points={
        'console_scripts': [
            'utopy_bot = utopy.utopy:main',
        ],
    },
    install_requires=["dataset", "steem==0.18.103", "pymysql"]
)