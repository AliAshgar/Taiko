from utils.logger import logger
from utils.web import web3Taiko, balance
from utils.config import load_config
from utils.kelas import InputValidator, Loader
from utils.bot import send_message
from utils.fungsi import eth_to_usd, clear, taiko_rank, DateConverter
from prompt_toolkit.shortcuts import PromptSession
import asyncio, random

async def proses():
    print("-" * 60)
    print("-                 Push Point Taiko Blazer                  -")
    print("-" * 60)
    print("-                     Pilih Mode Operasi                   -")
    print("-            1. Send Message          2. Init              -")
    print("-            3. ProcessMessage        4. Random            -")
    print("-" * 60)
    session = PromptSession()  
    mode_choice = int(await session.prompt_async("Masukkan Mode (1-4): ", validator=InputValidator("range")))
    clear(mode_choice)
    num_txs = int(await session.prompt_async("Masukkan jumlah transaksi:  ", validator=InputValidator("digit")))
    clear(num_txs)
    MinMaxdelay = await session.prompt_async("Masukkan rentang delay per transaksi (contoh: 20-60): ", validator=InputValidator("delay"))
    min_delay, max_delay = map(int, MinMaxdelay.split('-'))
    clear(MinMaxdelay)
    gwei_input = float(await session.prompt_async("Masukkan nilai gwei untuk transaksi (contoh: 0.09): ", validator=InputValidator("gwei")))
    clear(gwei_input)
    account_address = await session.prompt_async("Masukkan alamat wallet (contoh: 0x1A3F): ", validator=InputValidator("hexadecimal"))
    clear(account_address)
    private_key = await session.prompt_async("Masukkan private key (contoh: 0x1D3C): ", validator=InputValidator("hexadecimal"))
    clear(private_key)
    while True:
        countbot =  0
        date = DateConverter()
        saldoawal = balance(account_address)
        print(f'Jam: {date["time"]}', end='\r')
        if "08:30:00 AM" in date["time"]:
            for count in range(num_txs):
                notif = load_config('bot_notif')
                countbot += 1
                count += 1
                if count == 1 and notif: await send_message(f'Info; ({num_txs} tx/day)\n{date["all"]}\n{taiko_rank(account_address)}\nBalance: {eth_to_usd(saldoawal)}','Markdown')
                randomDelay = round(random.uniform(min_delay, max_delay))
                mode_c = random.choice([1, 2, 3]) if mode_choice == 4 else mode_choice
                await web3Taiko(count, account_address, private_key, gwei_input, mode_c)
                if countbot >= 10 and notif:
                    countbot = 0 
                    jam = DateConverter()
                    await send_message(f'TX: ({count}/{num_txs})\nJam: {jam["time"]}\n{taiko_rank(account_address)}\nSaldo: {eth_to_usd(balance(account_address))}','Markdown')
                elif count >= num_txs:
                    count = 0
                    saldoakhir = balance(account_address)
                    jam = DateConverter()
                    saldo = saldoakhir - saldoawal
                    logger.info(f'Proses transaksi sebanyak {num_txs} kali sudah selesai')
                    if notif: await send_message(f'TX: ({count}/{num_txs})\n{jam["all"]}\n{taiko_rank(account_address)}\nSaldo Awal: {eth_to_usd(saldoawal)}\nSaldo Akhir: {eth_to_usd(saldoakhir)}\nSaldo terpakai: {eth_to_usd(saldo)}','Markdown')
                else:
                    with Loader(f"Mohon tunggu.", '', randomDelay):
                        await asyncio.sleep(randomDelay)
        await asyncio.sleep(1)