#!/usr/bin/python3

from tools import helper


async def get_state(length):
    return await helper.create_access_token({'state': await helper.set_random_str(length)})
