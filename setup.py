import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


kwds = {}
try:
    kwds['long_description'] = open('README.rst').read()
except IOError:
    pass

# Read version from perfect_hash/__init__.py
pat = re.compile(r'__version__\s*=\s*(\S+)', re.M)
data = open('perfect_hash.py').read()
kwds['version'] = eval(pat.search(data).group(1))


setup(
    name = "perfect-hash",
    author = "Ilan Schnell",
    author_email = "ilanschnell@gmail.com",
    url = "https://github.com/ilanschnell/perfect-hash",
    license = "BSD",
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    description = "creating perfect minimal hash function",
    py_modules = ["perfect_hash"],
    scripts = ['perfect-hash'],
    **kwds
)
