#!/usr/bin/env python3
"""Defines a function make_multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns func to multiply the float"""
    return lambda x: x * multiplier
