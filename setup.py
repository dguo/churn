from setuptools import setup, find_packages

setup(
    name='churn',
    version='0.1.0',
    description='CLI for credit card payments and rewards',
    url='https://github.com/dguo/churn',
    author='Danny Guo',
    author_email='dannyguo91@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='credit card churning rewards',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=6,<7',
        'pick==0.6.1',
        'tabulate==0.7.7'
    ],
    entry_points={
        'console_scripts': [
            'churn=src.cli:main'
        ]
    }
)
