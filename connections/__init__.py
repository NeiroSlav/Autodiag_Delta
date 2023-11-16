from .switches.dlink import *
from .switches.zyxel import *
from .switches.bdcom import *
from .switches.foxgate import *
from .switches.raisecom import *

from .tolerance import Tolerance
from .telnet import Telnet

from .personal_data import *

switch_class = {
    'dlink': Dlink,
    'zyxel': Zyxel,
    'bdcom': Bdcom,
    'foxgate': Foxgate,
    'raisecom': Raisecom}
