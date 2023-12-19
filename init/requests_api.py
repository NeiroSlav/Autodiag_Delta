from datetime import datetime
import hashlib
import requests


def get_hash() -> str:
    dt = datetime.now().strftime("%Y-%m-%d %H")
    data = ('YBEgFxVl' + dt).encode(encoding='utf-8')
    return hashlib.md5(data).hexdigest()


def get_gcdb_data(anumber: str, switch_ip: str = ''):
    url = ['https://gcdbviewer.matrixhome.net/api_autodiag.php?action=get_by_anumber']
    url.append('hash=' + get_hash())
    url.append('anumber=' + anumber)
    url.append('switch=' + switch_ip)
    response = requests.get('&'.join(url))
    return response.json()


def set_gcdb_ticket(anumber: str, user: str, ticket_id: str, comment: str):
    url = ['https://gcdbviewer.matrixhome.net/api_autodiag.php?action=add_ticket']
    url.append('hash=' + get_hash())
    url.append('anumber=' + anumber)
    url.append('comment=' + comment)
    url.append('username=' + user)
    if ticket_id:
        url.append('group_ticket_id=' + ticket_id)

    print('&'.join(url))
    response = requests.get('&'.join(url))
    print(response)
    return {'ok': True}


def get_decview_status(switch_ip: str) -> str:
    url = 'https://decview.matrixhome.net/api/devices_rest/status/ipaddress/'
    response = requests.get(url + switch_ip).json()
    state = int(response['dev']['status'])
    time = response['dev']['timestamp']
    state = 'поднят' if state else 'лежит'
    return f'Свитч {switch_ip} {state} с {time}'