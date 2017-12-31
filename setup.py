from setuptools import setup, find_packages

setup(
    name='django-timer',
    description='A Django app implementing a timer model.',
    author='Martin Bierbaum',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    use_scm_version=True,
    setup_requires=[
        'setuptools_scm',
        ],
    install_requires=[
        'django>=1.11.4',
    ],
    python_requires='>=3.6.2',
)