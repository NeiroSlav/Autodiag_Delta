import requests

from ip_tools import fping
from connections.telnet import Telnet
from connections.switches.dlink import Dlink
from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.50.59'
    switch_port = 1


def switch_test():
    data = GcdbData()

    session = Telnet(data)
    print(session.switch_type)
    print(session.switch_model)

    switch = Dlink(session)
    print(switch.allowed_ports)
    # print(switch.set_port(GcdbData.switch_port, True))
    # print(switch.test_all(GcdbData.switch_port))
    # while True:


switch_test()
