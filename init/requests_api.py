from datetime import datetime
import hashlib
import requests



def get_gcdb_data(anumber: str, switch_ip: str = ''):
    url = ['https://gcdbviewer.matrixhome.net/api_autodiag.php?action=get_by_anumber']
    dt = datetime.now().strftime("%Y-%m-%d %H")
    data = ('YBEgFxVl' + dt).encode(encoding='utf-8')
    url.append('hash=' + hashlib.md5(data).hexdigest())
    url.append('anumber=' + anumber)
    url.append('switch=' + switch_ip)
    response = requests.request(method='GET', url='&'.join(url))
    return response.json()


def get_decview_status(switch_ip: str) -> str:
    decview_api = 'https://decview.matrixhome.net/api/devices_rest/status/ipaddress/'
    decview_info = requests.get(decview_api + switch_ip).json()
    state = int(decview_info['dev']['status'])
    time = decview_info['dev']['timestamp']
    state = 'поднят' if state else 'лежит'
    return f'Свитч {switch_ip} {state} с {time}'
