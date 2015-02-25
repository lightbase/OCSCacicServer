import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'requests',
    'chameleon',
    'ConfigParser'
]

setup(name='OCSCacicServer',
      version='0.1',
      description='OCSCacicServer',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Programming Language :: Python :: 3.4",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Lightbase',
      author_email='eduardo.santos@lighbase.com.br',
      url='',
      keywords='rest lightbase json cacic pyramid ocsinventory',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ocscacicserver',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = ocscacicserver:main
      [console_scripts]
      """
      )
