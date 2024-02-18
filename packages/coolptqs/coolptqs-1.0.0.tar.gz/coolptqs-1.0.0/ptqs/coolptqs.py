import datetime
import colored
import time
from time import sleep
from colored import fg, bg, attr

gray = fg("dark_gray")
reset = attr("reset")
purple = fg("purple_1a")

def info(message, with_loading=False):
    current_time = datetime.datetime.now().strftime(f"{gray}%H:%M:%S{reset}")
    if with_loading:
        print(f"{current_time} {purple}INF {gray}>{reset} {message}", end='', flush=True)
        for _ in range(3):
            sleep(0.2)
            print(".", end='', flush=True)
        print()
    else:
        print(f"{current_time} {purple}INF {gray}>{reset} {message}")

def debug(message, with_loading=False):
    current_time = datetime.datetime.now().strftime(f"{gray}%H:%M:%S{reset}")
    if with_loading:
        print(f"{current_time} {purple}DBG {gray}>{reset} {message}", end='', flush=True)
        for _ in range(3):
            sleep(0.2) 
            print(".", end='', flush=True)
        print()  
    else:
        print(f"{current_time} {purple}DBG {gray}>{reset} {message}")

def link(url, message):
    current_time = datetime.datetime.now().strftime(f"{attr("bold")}{gray}%H:%M:%S{reset}{attr("reset")}")
    clickable_link = f"\033]8;;{url}\033\\{message}\033]8;;\033\\"
    print(f"{current_time} {purple}INF {gray}>{reset} {clickable_link}")