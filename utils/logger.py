from loguru import logger
import sys
# Menghapus konfigurasi handler default
logger.remove()

# Menambahkan konfigurasi handler baru dengan format dan warna
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:DD-MM-YYYY HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)