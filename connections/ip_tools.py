import os
import re
import subprocess
import time
from sys import platform
import requests
from random import randint


class IterPing:

    def __init__(self, ip_address):
        self.ping_dict = {'lost': 0, 'pkg': []}
        self.command = ['fping', '--count=1', '--timeout=150', '--size=1450', ip_address]
        self.result = {'sent': 0, 'lost': 0, 'stats': {}}

    #  пинг утилитой fping по одному пакету
    def ping(self) -> dict:
        self.result['sent'] += 1
        try:
            answer = subprocess.check_output(self.command)
            # print(answer)
            answer = str(answer).split('ms')[0].split()[-1]
            self.ping_dict['pkg'].append(float(answer))
            return {'ok': True, 'answer': int(float(answer))}
        #  если пинг не прошёл
        except Exception as ex:
            # print(ex)
            self.ping_dict['lost'] += 1
            return {'ok': False}

    #  вычисляет финальные показатели пинга
    def get_result(self) -> dict:
        res, pd = self.result, self.ping_dict

        if not pd['pkg']:
            res['lost'] = 100
            res['ok'] = False
            return res

        res['stats']['min'] = int(min(pd['pkg']))
        res['stats']['avg'] = int(sum(pd['pkg']) / (len(pd['pkg'])))
        res['stats']['max'] = int(max(pd['pkg']))

        res['ok'] = not pd['lost']
        res['lost_percent'] = int(pd['lost']/res['sent'] * 100)

        return res


#  пинг свитча, проверка на доступность
def fping(ip_address: str) -> bool:
    if platform == "win32":  # для тестов с винды
        return True

    res = os.system(f"fping -c1 -t500 {ip_address}")
    # print('res =', res)
    if res != 0:  # если один пакет не прошёл, пробует ещё два с таймаутом 1сек
        res = os.system(f"fping -c2 -t1000 {ip_address}")
        if res != 0:
            return False
    return True


#  ищет открытые порты
def nmap(ip_address: str) -> dict:
    if platform == "win32":  # для тестов с винды
        return {'ip': ip_address, 'port': '228', 'protocol': 'http'}

    result = {'ip': ip_address, 'port': None, 'protocol': None}
    command = f"nmap -Pn --max-retries 1 --min-rate 30 --max-parallelism 20 -T4 " \
              f"-p 80,8080,90,9090,1080,8000,9000,666,8888,9091,4978 {ip_address}"

    answer = subprocess.check_output(command, shell=True)
    answer = str(answer).replace('\\n', '\n')
    answer = re.search(r'[0-9]+/tcp +open +[a-z]+', answer)  # ищет открытый порт
    if not answer:  # если порт не найден
        return result

    result['port'] = answer.group(0).split('/')[0]

    try:  # попытка запроса на http, если не удалось - https
        requests.get(f'https://{ip_address}:{result["port"]}/', timeout=1)
        result['protocol'] = 'https'
    except Exception:
        result['protocol'] = 'http'
    return result


#


if __name__ == '__main__':
    pass
    # result = nmap('192.168.0.1')
    # print()
    #
    # start_time = time.time()
    # nmap('192.168.0.1')
    # print("--- %s секунд ---" % (time.time() - start_time))

    # ping = IterPing('109.254.80.74')  # не пингается
    # # ping = IterPing('109.254.80.41')  # пингается
    # print('='*50)
    #
    # for i in range(10):
    #     print(ping.ping())
    #
    # print('='*50)
    # print(ping.get_result())
