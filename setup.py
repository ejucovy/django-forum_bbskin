from setuptools import setup, find_packages
import sys, os

version = '0.1'

readme = open('README.txt').read()

setup(name='django-forum_bbskin',
      version=version,
      description="a layer on top of django-forum to make it more BB-like",
      long_description=readme,
      classifiers=['Framework :: Django'],
      keywords='django django-forum',
      author='Ethan Jucovy',
      author_email='ethan.jucovy@gmail.com',
      url='',
      license='GPLv3 or greater',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      #dependency_links=[
      #  'http://django-forum.googlecode.com/svn/trunk/#egg=django-forum'
      #],
      install_requires=[
          'djangohelpers',
      #    'django-forum',
      ],
      entry_points="""
      """,
      )
