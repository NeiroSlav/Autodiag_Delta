from connections.telnet import Telnet
from structure.connections.switches.dlink import Dlink
from structure.connections.switches.raisecom import Raisecom
from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.69.183'
    switch_port = 2


data = GcdbData()

session = Telnet(data)
switch = Raisecom(session)

# print(switch.set_port(GcdbData.switch_port, True))
print(switch.test_all(GcdbData.switch_port))
