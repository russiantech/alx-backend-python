#!/usr/bin/env python3
"""Makes an asynchronous coroutine function"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Waits for a random delay b/w 0 & max_delay"""
    random_number = random.uniform(0, max_delay)
    await asyncio.sleep(random_number)
    return random_number
