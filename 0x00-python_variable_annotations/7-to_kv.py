#!/usr/bin/env python3
"""Defines a function to_kv"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Returns tuple of str & float"""
    x = v ** 2
    return (k, x)
