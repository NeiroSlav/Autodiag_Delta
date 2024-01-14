import os
import re
import subprocess
import time
from random import randint


class IterPing:
    stat_keys = ['min', 'avg', 'max']

    def __init__(self, ip_address):
        self.ping_dict = {'lost': 0, 'min': [], 'avg': [], 'max': []}
        self.command = ['ping', '-c1', ip_address]
        self.result = {'sent': 0, 'loss': 0.0, 'stats': {}}

    #  пинг утилитой ping по одному пакету
    def ping(self) -> dict:
        self.result['sent'] += 1
        try:
            answer = subprocess.check_output(self.command)
            answer = str(answer).split()[-2].split('/')
            answer = {self.stat_keys[j]: float(answer[j]) for j in range(3)}
            for key in self.stat_keys:
                self.ping_dict[key].append(answer[key])
            return answer | {'ok': True}
        #  если пинг не прошёл
        except subprocess.CalledProcessError:
            self.ping_dict['loss'] += 1
            return {'ok': False}

    #  вычисляет финальные показатели пинга
    def get_result(self) -> dict:
        res, pd = self.result, self.ping_dict

        res['stats']['min'] = round(min(pd['min']), 2)
        res['stats']['avg'] = round(sum(pd['avg']) / (len(pd['avg'])), 2)
        res['stats']['max'] = round(max(pd['max']), 2)

        res['ok'] = not pd['lost']
        res['loss'] = pd['lost']/res['sent'] * 100

        return res


#  пинг утилитой fping (очень быстрый)
def fping(ip_address: str) -> bool:
    res = os.system(f"fping -c1 -t500 {ip_address}")
    print('res =', res)
    if res != 0:  # если один пакет не прошёл, пробует ещё два с таймаутом 1сек
        res = os.system(f"fping -c2 -t1000 {ip_address}")
        if res != 0:
            return False
    return True


#  ищет открытые порты
def nmap(ip_address: str) -> dict:
    command = f"nmap -PN -p 80,8080,90,9090,1080,8000,9000,666,8888,9091,4978 {ip_address}"
    answer = subprocess.check_output(command, shell=True)
    answer = str(answer).replace('\\n', '\n')

    port = re.search(r'[0-9]+/tcp +open', answer)  # ищет открытый порт
    if not port:  # если порт не найден
        return {'ip': ip_address, 'port': None}

    port = port.group(0).split('/')[0]
    return {'ip': ip_address, 'port': port}

    # return {'ip': ip_address, 'port': '9090'}


if __name__ == '__main__':
    ping = IterPing('google.com')
    print('='*50)

    for i in range(10):
        print(ping.ping())

    print('='*50)
    print(ping.get_result())
    print(ping.result)
