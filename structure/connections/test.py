from connections.telnet import Telnet
from structure.connections.switches.dlink import Dlink

from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.32.135'
    switch_port = 12


data = GcdbData()

session = Telnet(data)
switch = Dlink(session)

print(switch.log(GcdbData.switch_port))
