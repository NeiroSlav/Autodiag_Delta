import requests
from pprint import pprint
from switches.utils.switches_ip import dlink_ip
from ip_tools import fping
from connections.telnet import Telnet
from connections.switches.dlink import Dlink
from connections.switches.bdcom_fe import BdcomFE
from personal_data import switch_login, switch_password
from datetime import datetime
import hashlib


#
def get_gcdb_data(anumber: str, switch: str = ''):
    url = ['https://gcdbviewer.matrixhome.net/api_autodiag.php?action=get_by_anumber']
    dt = datetime.now().strftime("%Y-%m-%d %H")
    data = ('YBEgFxVl' + dt).encode(encoding='utf-8')
    url.append('hash='+hashlib.md5(data).hexdigest())
    url.append('anumber='+anumber)
    if switch:
        url.append('switch='+switch)

    r = requests.request(method='GET', url='&'.join(url))
    print(r)

    if r:
        print('good')
    else:
        print('bad')

    return r


class GcdbData:
    def __init__(self, ip):
        self.username = 'aboba'
        self.switch_ip = ip
        self.switch_port = 1
        self.pon_port = 0
        self.switch_login = switch_login
        self.switch_password = switch_password


def switch_test():
    # for elem in dlink_ip:
    
    gcdb_data = GcdbData('192.168.50.220')
    telnet_session = Telnet(gcdb_data)
    switch = BdcomFE(telnet_session)
    print(switch.port(7))
    print(switch.mac(5, ['ac:84:c6:e7:72:6d']))


switch_test()
