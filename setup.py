from setuptools import setup, find_packages
import sys
import os

version = '0.1'

setup(name='rcnova',
      version=version,
      description="Extensions to the nova api for the NeCTAR project.",
      long_description="""\
""",
      classifiers=[],  # Get strings from
                       # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Russell Sim',
      author_email='russell.sim@gmail.com',
      url='http://nectar.org.au/',
      license='Apache License (2.0)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
