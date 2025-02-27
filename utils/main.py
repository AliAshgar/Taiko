from utils.logger import logger
from utils.web import web3Taiko, balance, find_address
from utils.kelas import InputValidator, Loader
from utils.bot import send_message
from utils.fungsi import eth_to_usd, clear, taiko_rank, DateConverter
from prompt_toolkit.shortcuts import PromptSession
from utils.config import load_config, write_config
import asyncio, random

async def proses():
    print("-" * 60)
    print("-                 Push Point Taiko Blazer                  -")
    print("-" * 60)
    print("-                     Pilih Mode Operasi                   -")
    print("-            1. Send Message          2. Init              -")
    print("-            3. ProcessMessage        4. Random            -")
    print("-" * 60)
    print("-" * 60)

    session = PromptSession()  
    mode_choice = int(await session.prompt_async("Masukkan Mode (1-4): ", validator=InputValidator("range")))
    num_txs = int(await session.prompt_async("Masukkan jumlah transaksi:  ", validator=InputValidator("digit")))
    min_delay, max_delay = map(int, (await session.prompt_async("Masukkan rentang delay per transaksi (contoh: 20-60): ", validator=InputValidator("delay"))).split("-"))
    gwei_input = float(await session.prompt_async("Masukkan nilai gwei untuk transaksi (contoh: 0.09): ", validator=InputValidator("gwei")))
    while True:
        private_key = await session.prompt_async("Masukkan private key (contoh: 0x1D3C): ", validator=InputValidator("hexadecimal"))
        clear(private_key)
        try:
            account_address = find_address(private_key)
            print(f'Anda menggunakan Acoount Address: {account_address}')
            break
        except:
            print(f"Tidak ditemukannya Address pada Private Key: {private_key[:6]}....{private_key[-6:]}")
    run_time = DateConverter()
    print(f'Running Time in next time: {run_time["run_time"]}')
    load = load_config()
    load['run_time'] = run_time['run_time']
    write_config(load)
    while True:
        countbot =  0
        date = DateConverter()
        load_run = load_config("run_time")
        saldoawal = balance(account_address)
        print(f'Jam: {date["time"]} run: {load_run}', end='\r')
        if load_run in date["run_time"]:
            for count in range(num_txs):
                countbot += 1
                count += 1
                if count == 1: await send_message(f'Info; ({num_txs} tx/day)\n{date["all"]}\n{taiko_rank(account_address)}\nBalance: {eth_to_usd(saldoawal)}','Markdown')
                randomDelay = round(random.uniform(min_delay, max_delay))
                mode_c = random.choice([1, 2, 3]) if mode_choice == 4 else mode_choice
                await web3Taiko(count, account_address, private_key, gwei_input, mode_c)
                if countbot >= 10:
                    countbot = 0 
                    jam = DateConverter()
                    await send_message(f'TX: ({count}/{num_txs})\nJam: {jam["time"]}\n{taiko_rank(account_address)}\nSaldo: {eth_to_usd(balance(account_address))}','Markdown')
                elif count >= num_txs:
                    saldoakhir = balance(account_address)
                    jam = DateConverter()
                    saldo = saldoakhir - saldoawal
                    logger.info(f'Proses transaksi sebanyak {num_txs} kali sudah selesai')
                    await send_message(f'TX: ({count}/{num_txs})\n{jam["all"]}\n{taiko_rank(account_address)}\nSaldo Awal: {eth_to_usd(saldoawal)}\nSaldo Akhir: {eth_to_usd(saldoakhir)}\nSaldo terpakai: {eth_to_usd(saldo)}','Markdown')
                    count = 0
                else:
                    with Loader(f"Please Wait....", '', randomDelay):
                        await asyncio.sleep(randomDelay)
        await asyncio.sleep(1)