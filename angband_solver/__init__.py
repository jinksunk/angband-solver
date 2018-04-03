"""
Load a model of the equipment set to optimize, along with scoring and
constraint data, and return a yaml document describing the optimal equipment
set, along with other information.
"""

from .solver import optimize

__all__ = ['optimize']
