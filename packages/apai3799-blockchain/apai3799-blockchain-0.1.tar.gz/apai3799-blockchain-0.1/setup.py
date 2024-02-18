from setuptools import setup, find_packages

setup(name='apai3799-blockchain',
      version='0.1',
      url='https://github.com/jkjk101/pyblockchain',
      license='MIT',
      author='jkjk101',
      author_email='jksm101852@gmail.com',
      description='A simple python blockchain package',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
