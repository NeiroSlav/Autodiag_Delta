from datetime import datetime
import hashlib
import requests


class GcdbApi:
    url = 'https://gcdbviewer.matrixhome.net/api_autodiag.php?action=get_by_anumber'

    # создание хеша для запроса
    @staticmethod
    def _get_hash() -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H")
        data = ('YBEgFxVl' + dt).encode(encoding='utf-8')
        return hashlib.md5(data).hexdigest()

    # запрос достаёт данные из gcdb по лс
    @staticmethod
    def get_data(anumber: str, switch_ip: str = ''):
        url = [GcdbApi.url,
               'hash=' + GcdbApi._get_hash(),
               'action=get_by_anumber',
               'anumber='+anumber,
               'switch='+switch_ip]
        # print('&'.join(url))
        response = requests.get('&'.join(url))
        if response.status_code != 200:
            return None

        # print(response)
        return response.json()

    # запрос создаёт тикет
    @staticmethod
    def set_ticket(anumber: str, user: str, ticket_id: str, comment: str):
        url = [GcdbApi.url,
               'hash=' + GcdbApi._get_hash(),
               'action=add_ticket',
               'anumber='+anumber,
               'comment='+comment,
               'username='+user,
               'dup=1']
        if ticket_id:
            url.append('group_ticket_id=' + ticket_id)

        status = bool(requests.get('&'.join(url)))
        return {'ok': status}


class DecviewApi:
    url = 'https://decview.matrixhome.net/api/devices_rest/status/ipaddress/'

    @staticmethod
    def get_status(switch_ip: str) -> str:
        url = DecviewApi.url
        response = (requests.get(url + switch_ip))
        if response.status_code != 200:
            return f'Ошибка запроса на DecView, статус: {response.status_code}'

        response = response.json()
        state = int(response['dev']['status'])
        time = response['dev']['timestamp']
        state = 'поднят' if state else 'лежит'
        return f'Свитч {switch_ip} {state} с {time}'


if __name__ == '__main__':
    ls, ip = '0203134133', '192.168.35.43'
    print(GcdbApi.get_data(ls, ip))
