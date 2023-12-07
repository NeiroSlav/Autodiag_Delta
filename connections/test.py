import requests
from switches.utils.switches_ip import dlink_ip
from ip_tools import fping
from connections.telnet import Telnet
from connections.switches.dlink import Dlink
from personal_data import switch_login, switch_password


class GcdbData:
    switch_login = switch_login
    switch_password = switch_password
    switch_ip = '192.168.44.131'
    switch_port = 16


def switch_test():
    data = GcdbData()

    for ip in dlink_ip:
        data.switch_ip = ip

        session = Telnet(data)
        print(session.switch_type)
        print(session.switch_model)
        print(session.switch_ip)
        #
        switch = Dlink(session)

        print(switch.bind_state(1))
        # ports = int(session.switch_model[-2] + session.switch_model[-1])
        # for i in range(1, ports):
        #     print(switch.errors(i))


switch_test()
