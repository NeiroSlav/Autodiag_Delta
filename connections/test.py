import requests
from switches.utils.switches_ip import dlink_ip
from ip_tools import fping
from connections.telnet import Telnet
from connections.switches.dlink import Dlink
from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.30.60'
    switch_port = 9


def switch_test():
    data = GcdbData()

    for ip in dlink_ip:
        data.switch_ip = ip

        session = Telnet(data)
        print(session.switch_type)
        print(session.switch_model)
        #
        switch = Dlink(session)
        ports = int(session.switch_model[-2] + session.switch_model[-1])
        for i in range(1, ports):
            print(switch.errors(i))


switch_test()
