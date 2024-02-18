from setuptools import find_packages, setup

setup(
    name='olscrypto',
    packages=find_packages(),
    version='0.1.0',
    description='OLS Crypto Library',
    author='Highmaru, Inc.',
    author_email="dhshin@highmaru.com",
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests'
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)