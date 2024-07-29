from colorama import Fore
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
from prompt_toolkit.validation import Validator, ValidationError

class InputValidator(Validator):
    def __init__(self, validation_types):
        super().__init__()
        self.validation_types = validation_types.split(", ")

    def validate(self, document):
        text = document.text.strip()

        if "digit" in self.validation_types:
            if not text.isdigit():
                raise ValidationError(message='Input harus berupa angka', cursor_position=len(text))

        if "range" in self.validation_types:
            if not text.isdigit() or int(text) not in [1, 2, 3, 4]:
                raise ValidationError(message='Input anda tidak sesuai. Harus antara 1 dan 4', cursor_position=len(text))

        if "hexadecimal" in self.validation_types:
            if not text.startswith("0x") or len(text) <= 2:
                raise ValidationError(message='Input harus diawali dengan "0x" dan tidak boleh kosong', cursor_position=len(text))
            try:
                int(text, 16)  # Mengkonversi string ke integer dengan basis 16 (heksadesimal)
            except ValueError:
                raise ValidationError(message='Input harus berupa angka heksadesimal yang valid setelah "0x"', cursor_position=len(text))

        if "mode" in self.validation_types:
            if not text:
                raise ValidationError(message='Input tidak boleh kosong', cursor_position=len(text))

        if "delay" in self.validation_types:
            try:
                min_delay, max_delay = map(int, text.split('-'))
                # Menambahkan validasi untuk memastikan input adalah dua angka
                if not all(x.isdigit() for x in text.split('-')):
                    raise ValidationError(message='Input harus berupa dua angka yang dipisahkan oleh tanda "-"', cursor_position=len(text))
                if min_delay < 0 or max_delay < 0:
                    raise ValidationError(message='Delay harus lebih besar atau sama dengan 0', cursor_position=len(text))
                if min_delay >= max_delay:
                    raise ValidationError(message='max_delay harus lebih besar dari min_delay', cursor_position=len(text))
            except ValueError:
                raise ValidationError(message='Input harus berupa dua angka yang dipisahkan oleh tanda "-"', cursor_position=len(text))
            map(int, text.split('-'))

        if "gwei" in self.validation_types:
            try:
                value = float(text)
                if value < 0:
                    raise ValidationError(message='Nilai gwei harus lebih besar atau sama dengan 0', cursor_position=len(text))
            except ValueError:
                raise ValidationError(message='Input harus berupa angka desimal yang valid', cursor_position=len(text))

        if all(v_type not in self.validation_types for v_type in ["digit", "range", "hexadecimal", "mode", "delay", "gwei"]):
            raise ValidationError(message='Tipe validasi tidak dikenali', cursor_position=len(text))
        
class Loader:
    def __init__(self, desc="Loading....", end="", delay=0, timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        self.done = False
        self.delay = delay

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        i = 1
        for c in cycle(self.steps):
            i += self.timeout
            if self.done:
                break
            print(f"\r{Fore.YELLOW}[Waiting]{Fore.RESET} {self.desc} -> {c} {Fore.LIGHTGREEN_EX}{round(self.delay-i) if self.delay else round(i)}{Fore.RESET}s.", end="\r")
            sleep(self.timeout)

    def __enter__(self):
        self.start()
        return self

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()