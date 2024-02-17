
#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(name='simple-pyper',
      version=VERSION,
      description="a tiny cli tool for using any python file esaily.",
      long_description='just enjoy',
      classifiers=[], 
      author='chen',
      author_email='c1556613010@outlook.com',
      url='https://github.com/chenyiru3/simple-pyper',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'pyper = simple_pyper:run_cmd'
        ]
      },
)

