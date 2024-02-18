"""
Copyright (c) 2023 Adrian Price-Whelan. All rights reserved.

pyia: A Python package for working with data from the Gaia mission
"""


from . import data
from ._version import version as __version__
from .data import GaiaData

__all__ = ["__version__", "GaiaData", "data"]
