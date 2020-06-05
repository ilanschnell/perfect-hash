import re
from distutils.core import setup


kwds = {}
try:
    kwds['long_description'] = open('README.md').read()
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
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    description = "creating perfect minimal hash function",
    py_modules = ["perfect_hash"],
    scripts = ['perfect-hash'],
    **kwds
)
