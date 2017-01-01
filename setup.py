from setuptools import setup, find_packages

setup(
    name='churn',
    version='0.1.0',
    description='CLI for credit card payments and rewards',
    url='https://github.com/dguo/churn',
    author='Danny Guo',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Organisational :: Financial',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='credit card churning rewards',
    packages=find_packages(),
    install_requires=[
        'click>=6'
    ],
    py_modules=['churn'],
    entry_points={
        'console_scripts': [
            'churn=churn:cli'
        ]
    }
)

