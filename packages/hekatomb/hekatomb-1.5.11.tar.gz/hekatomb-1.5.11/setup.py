try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='hekatomb',
    version='1.5.11',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=[
        'src',
    ],
    license='GPL-3.0 license',
    author="Processus Thief",
    author_email='hekatomb@thiefin.fr',
    url='https://github.com/ProcessusT/HEKATOMB',
    keywords='dpapi windows blob masterkey activedirectory credentials',
    install_requires=[
      'pycryptodomex',
      'impacket',
      'dnspython',
      'ldap3'
    ],
    python_requires='>=3.6',
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
     ),
)
