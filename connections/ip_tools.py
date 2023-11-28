import os


def ping(ip_address: str) -> bool:
    return os.system(f"ping -i .2 -s 1000 -c 3 {ip_address}")