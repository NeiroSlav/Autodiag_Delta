import os
import re
import subprocess


#  пинг утилитой fping (очень быстрый)
def fping(ip_address: str) -> bool:
    res = os.system(f"fping -c1 -t500 {ip_address}")
    print('res =', res)
    if res != 0:  # если один пакет не прошёл, пробует ещё два с таймаутом 1сек
        res = os.system(f"fping -c2 -t1000 {ip_address}")
        if res != 0:
            return False
    return True


def nmap(ip_address: str) -> dict:
    command = f"nmap -PN -p 80,8080,90,9090,1080,8000,9000,666,8888,9091,4978 {ip_address}"
    answer = subprocess.check_output(command, shell=True)
    answer = str(answer).replace('\\n', '\n')

    port = re.search(r'[0-9]+/tcp +open', answer)  # ищет открытый порт
    if not port:  # если порт не найден
        return {'ip': ip_address, 'port': None}

    port = port.group(0).split('/')[0]
    return {'ip': ip_address, 'port': port}
