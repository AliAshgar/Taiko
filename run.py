import asyncio
from utils.main import proses

try:
    # Cek apakah event loop sudah berjalan
    loop = asyncio.get_running_loop()
    # Jika event loop sudah berjalan, gunakan await
    asyncio.ensure_future(proses())
except RuntimeError:
    # Jika event loop belum berjalan, gunakan asyncio.run()
    asyncio.run(proses())