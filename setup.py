from distutils.core import setup

setup(
    name='cryptocompare',
    version='0.1',
    packages=['cryptocompare'],
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['requests >= 2.0.0']
)
