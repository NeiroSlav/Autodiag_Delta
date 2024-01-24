from .switches.dlink import *
from .switches.zyxel import *
from .switches.bdcom import *
from .switches.foxgate import *
from .switches.raisecom import *
from .switches.bdcom_fe import *

from .ip_tools import fping, nmap, IterPing
from .telnet import Telnet

from .personal_data import *

_switch = {
    'dlink': Dlink,
    'dlink1210': Dlink1210,
    'zyxel': Zyxel,
    'bdcom': Bdcom,
    'bdcom_fe': BdcomFE,
    'foxgate': Foxgate,
    'raisecom': Raisecom}
