#!/usr/bin/env python3
"""sum_list(input_list[])"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Returns sum of float in a list"""
    a: float = 0.0
    for i in input_list:
        a += i
    return a
