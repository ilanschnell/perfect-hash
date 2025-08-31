from setuptools import setup, Extension

setup(
    ext_modules = [
        Extension(name = "stations",
                  sources = ["stations.c"])
    ]
)
