import asyncio

import config
import database

from random import randint

from TonTools import *

async def main():
    try:
        open('database.db')
        print('Database already exists')
        exit()
    except FileNotFoundError:
        print('Creating database...')

    client = TonCenterClient(
        key=config.TONCENTER_API, 
        orbs_access=True,
        testnet=config.TESTNET)

    data = await client.get_collection(collection_address=config.COLLECTION)
    items = await client.get_collection_items(collection=data, limit_per_one_request=50)

    tokens = []
    codes = []
    for item in items:
        tokens.append(item.address)
        code = randint(100000, 999999)
        if code not in codes:
            codes.append(code)

    database.create_db(tokens, codes)
        

if __name__ == '__main__':
    asyncio.run(main())

