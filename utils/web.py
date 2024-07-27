import asyncio
from web3 import Web3
from web3.middleware import geth_poa_middleware
from utils.logger import logger
from utils.config import load_config
from utils.kelas import Loader
from utils.fungsi import signature, msg, psnE, psnS, msgtypeTX
from utils.bot import send_message

def balance(address):
    try:
        w3 = Web3(Web3.HTTPProvider(load_config('taiko_url')))
        return w3.from_wei(w3.eth.get_balance(address), 'ether')
    except Exception as e:
        return str(e)

def find_address(private_key):
    return Web3().eth.account.from_key(private_key).address

async def web3Taiko(count, address, private_key, gwei, mode):
    retries = 0
    maxretries = 5
    rpc = load_config('taiko_url')
    while True:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            if not w3.is_connected():
                retries += 1
                logger.warning(f'Failed connect to RPC: {retries}/{maxretries}')
                if retries >= maxretries:
                    await send_message(f'Failed connect to RPC {retries}/{maxretries}')
                    exit()
                await asyncio.sleep(5)
            else:
                logger.info(f'{msgtypeTX(mode, count)}')
                logger.debug(f'Connected to RPC: {rpc}')
                nonce = w3.eth.get_transaction_count(address)
                logger.debug(f'Transaction Count in Blockchain: {nonce}')
                transaction = {
                    'from': address,
                    'to': '0x1670000000000000000000000000000000000001',
                    'nonce': nonce,
                    'gas': 23000,
                    'gasPrice': w3.to_wei(gwei, 'gwei'),
                    'chainId': 167000,
                    'value': w3.to_wei(0, 'ether'),
                    'data': signature(mode)  # Tambahkan log sebelum ini
                }
                signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                with Loader(f'{msg(mode)}'):  # Tambahkan log sebelum ini  # Log message
                    w3.eth.wait_for_transaction_receipt(tx_hash)
                    logger.success(f'{psnS(tx_hash.hex())}')
                break  # Tambahkan break untuk menyelesaikan blok
        except Exception as e:  # Log exception
            if "is not in the chain after 120 seconds" in str(e):
                retries += 1
                logger.warning(f'Info {retries}/{maxretries} | Message: {str(e)}')
                if retries >= maxretries: 
                    await send_message(f'Info: {retries}/{maxretries}\rError: {str(e)}')
                    logger.error(f'TX {count} | Error: {psnE(str(e))}')
                    exit()
                await asyncio.sleep(5)
            logger.error(f'TX {count} | Error: {psnE(str(e))}')
            await send_message(f'TX {count} | Error: {str(e)}')
            exit()

