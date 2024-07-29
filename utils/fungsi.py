import requests, sys, pytz
from time import sleep
from decimal import Decimal
from datetime import datetime

def taiko_rank(address):
    url = f'https://trailblazer.mainnet.taiko.xyz/user/rank?address={address}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return f"Account: [{address[:6]}....{address[-6:]}](https://trailblazers.taiko.xyz/profile/{address})\nRank: {data['rank']}/{data['total']}\nScore: {round(data['score'])}"
    else:
        return f"Gagal mengakses halaman, status code: {response.status_code}"

def eth_to_usd(eth_amount):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {'ids': 'ethereum', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    data = response.json()
    eth_to_usd_rate = data['ethereum']['usd']
    eth_amount = float(Decimal(eth_amount))
    eth_to_usd_value = eth_amount * eth_to_usd_rate
    return f'{eth_amount:.6f} ETH - (${eth_to_usd_value:.2f})'


def DateConverter(timezone_str='Asia/Jakarta'):
    # Mapping hari dan bulan dari bahasa Inggris ke bahasa Indonesia
    days_map = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }

    months_map = {
        'January': 'Januari',
        'February': 'Februari',
        'March': 'Maret',
        'April': 'April',
        'May': 'Mei',
        'June': 'Juni',
         'July': 'Juli',
        'August': 'Agustus',
        'September': 'September',
        'October': 'Oktober',
        'November': 'November',
        'December': 'Desember'  
    }
    # Dapatkan zona waktu
    timezone = pytz.timezone(timezone_str)
    date = datetime.now()

    # Konversi tanggal ke zona waktu yang diinginkan
    if date.tzinfo is None: local_date = timezone.localize(date)
    else: local_date = date.astimezone(timezone)
    
    # Dapatkan nama hari dan bulan dalam bahasa Inggris
    day_name = local_date.strftime('%A')
    month_name = local_date.strftime('%B')
    
    # Ubah nama hari dan bulan ke bahasa Indonesia
    day_name_id = days_map[day_name]
    month_name_id = months_map[month_name]
   
    # Format tanggal dalam bahasa Indonesia
    formatted_date = {}  # Inisialisasi dictionary
    formatted_date['day'] = f"{day_name_id}"
    formatted_date['date'] = f"{local_date.strftime('%d')} {month_name_id} {local_date.strftime('%Y')}"
    formatted_date['time'] = f"{local_date.strftime('%I:%M:%S %p')}"
    formatted_date['all'] = f"Hari: {day_name_id}, {local_date.strftime('%d')} {month_name_id} {local_date.strftime('%Y')}"
    formatted_date['run_time'] = f"{local_date.strftime('%H:%M')}"
    
    return formatted_date

def mode(value):
    return ['Send Message.', 'Init.', 'Process Message.', 'Random.'][value-1]

def msg(value):
    return ['Memulai mengirim pesan', 'Memulai inisialisasi Contract', 'Memulai memproses pesan'][value-1]

def signature(value):
    return ['0x1bdb0037', '0xf09a4016', '0x2035065e'][value-1]

def msgtypeTX(value, tx):
    return f"TXs <red>-></red> <yellow>{tx}</yellow> | Mode: <blue>{mode(value)}</blue>"

def psnE(psn):
    return f'<red>{psn}</red>'

def psnS(psn):
    return f"hash: <green>{psn}</green>"

def clear(input, slp=0):
    print(f'{input}')
    sleep(slp)
    sys.stdout.write("\033[F\033[K\033[F\033[K")



