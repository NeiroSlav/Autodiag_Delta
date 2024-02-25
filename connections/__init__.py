from .switches.dlink import *
from .switches.zyxel import *
from .switches.bdcom import *
from .switches.foxgate import *
from .switches.raisecom import *
from .switches.bdcom_fe import *
from .dhcp_tools import DhcpUnity

from .ip_tools import fping, nmap, IterPing
from .telnet import Telnet

from .personal_data import *

"""
Библиотека "connections" позволяет подключаться к различным свитчам, 
выполнять команды от лица пользователя.
Использовать следующим образом:

создаём объект класса Telnet:
telnet = Telnet('192.168.x.x)

передаём объект классу свитча:
switch = Dlink(telnet)

работаем с методами свитча:
Dlink.set_port(port=2, enable=False)
answer = Dlink.log()
"""

# ключ - тип свитча, значение - ссылка на класс
_switch = {
    'dlink': Dlink,
    'dlink1210': Dlink1210,
    'zyxel': Zyxel,
    'bdcom': Bdcom,
    'bdcom_fe': BdcomFE,
    'foxgate': Foxgate,
    'raisecom': Raisecom
}
