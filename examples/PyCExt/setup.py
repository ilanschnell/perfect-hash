try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    ext_modules = [
        Extension(name = "stations",
                  sources = ["stations.c"])
    ]
)
