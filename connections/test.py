from ip_tools import fping
from connections.telnet import Telnet
from connections.switches.dlink import Dlink
from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.48.173'
    switch_port = 20


def switch_test():
    data = GcdbData()

    session = Telnet(data)
    switch = Dlink(session)

    # print(switch.set_port(GcdbData.switch_port, True))
    # print(switch.test_all(GcdbData.switch_port))
    while True:
        print(switch.util(GcdbData.switch_port))


def fping_test():
    y = '192.168.60.178'
    n = '192.168.63.191'

    print(fping(y))
    print('\n' * 3)
    print(fping(n))
