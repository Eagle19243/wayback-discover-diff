from setuptools import setup, find_packages

setup(
    name='Wayback-discover-diff',
    version='0.1.2.2',
    description='Calculate wayback machine captures simhash',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Flask',
        'simhash',
        'redis',
        'urllib3',
        'PyYAML',
        'Celery',
        'gunicorn',
        'pytest',
        'xxhash',
        'beautifulsoup4',
        'lxml',
        'flask-cors'
        ],
    tests_require=[
        'pytest',
        'mock'
        ],
    )
