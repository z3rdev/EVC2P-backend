from typing import Union

from TonTools import *
from fastapi import FastAPI, HTTPException
import asyncio

import config
import database

app = FastAPI()

try:
    open('database.db')
except FileNotFoundError:
    print('Database does not exist. Run generate.py first.')
    exit()

@app.get("/send")
def send(code: str, wallet: str):
    token = database.get_token(code, wallet)
    if token is None:
        raise HTTPException(status_code=401, detail="Already used code or wallet")
    print(token)
    token = Address(token).to_string(is_user_friendly=True, is_test_only=config.TESTNET)
    print(token)
    personal = False
    if token.startswith('EQ'):
        personal = True
    
    print('Init client')
    client = TonCenterClient(
        key=config.TONCENTER_API, 
        orbs_access=True,
        testnet=config.TESTNET)
    
    print('Init wallet')
    operation_wallet = Wallet(provider=client, mnemonics=config.MNEMONIC, version='v4r2')
    
    print('Sending...')
    try:
        resp = asyncio.run(operation_wallet.transfer_nft(destination_address=wallet, nft_address=token, fee=0.1))
        print(resp)
        if resp != 200:
            raise Exception('Operation wallet transaction error')
        return {"response": resp}
    except Exception as e:
        if personal is False:
            database.undo(token, code, wallet)
        raise HTTPException(status_code=500, detail='Sending error, try again! ' + str(e))