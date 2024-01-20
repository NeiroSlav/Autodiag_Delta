import hashlib
from datetime import datetime
from pprint import pprint

import requests


class GcdbApi:
    url = 'https://gcdbviewer.matrixhome.net/api_autodiag.php?action='

    # создание хеша для запроса
    @staticmethod
    def _get_hash() -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H")
        data = ('YBEgFxVl' + dt).encode(encoding='utf-8')
        return hashlib.md5(data).hexdigest()

    # запрос достаёт данные из gcdb по лс
    @staticmethod
    def get_data(anumber: str, switch_ip: str = ''):
        url = [GcdbApi.url + 'get_by_anumber',
               'hash=' + GcdbApi._get_hash(),
               'anumber='+anumber,
               'switch='+switch_ip,
               'new=1']
        # print('&'.join(url))
        response = requests.get('&'.join(url))
        if response.status_code != 200:
            return None

        # print(response)
        return response.json()

    # запрос создаёт тикет
    @staticmethod
    def set_ticket(anumber: str, user: str, ticket_id: str, comment: str):
        url = [GcdbApi.url + 'add_ticket',
               'hash=' + GcdbApi._get_hash(),
               'anumber='+anumber,
               'username='+user,
               'dup=1']

        if ticket_id:
            url.append('group_ticket_id=' + ticket_id)
            comment = 'групповая ' + ticket_id

        url.append('comment='+comment)

        # pprint(url)
        # print('&'.join(url))
        # return {'ok': True}
        status = bool(requests.get('&'.join(url)))
        return {'ok': status}


class DecviewApi:
    url = 'https://decview.matrixhome.net/api/devices_rest/status/ipaddress/'

    @staticmethod
    def get_status(switch_ip: str) -> dict:
        result = {'state': '', 'log': []}
        status_map = {'30': 'упал',
                      '40': 'поднялся',
                      # '50': 'не в эксп.',
                      '1': 'работает'}

        # обращается к api, забирает данные
        response = (requests.get(DecviewApi.url + switch_ip))
        if response.status_code != 200:
            result['state'] = f'Ошибка запроса DecView: {response.status_code}'
            return result

        response = response.json()

        # создаёт текущее состояние свитча
        status = int(response['dev']['status'])
        status = "поднят" if status else "лежит"
        time = response['dev']['timestamp']
        result['state'] = f'Свитч {switch_ip} {status} с {time}'

        # создаёт лог падений свитча
        for elem in response['log']:
            try:
                status = status_map[elem['status']]
                time = elem['timestamp']
                elem = f'{time} {status}'
                result['log'].append(elem)
            except KeyError:
                result['log'].append('неизвестный статус')

        return result


if __name__ == '__main__':
    ls, ip = '0104003018', '192.168.44.160'
    pprint(GcdbApi.get_data(ls, ip))
    pprint(DecviewApi.get_status(ip))
