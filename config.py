from dotenv import load_dotenv
import os

load_dotenv()

TONCENTER_API = os.environ['TONCENTER_API']
COLLECTION = os.environ['COLLECTION']

MNEMONIC = os.environ['MNEMONIC'].split(' ')

TESTNET = os.environ['TESTNET'] == 'True'