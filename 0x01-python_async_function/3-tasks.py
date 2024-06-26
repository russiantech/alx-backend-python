#!/usr/bin/env python3
"""Creates a task here"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Returns a task here"""
    return asyncio.create_task(wait_random(max_delay))
