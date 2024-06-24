from connections import Telnet, Dlink


def switch_test():
    telnet_session = Telnet(switch_ip='192.168.31.111')
    switch = Dlink(telnet_session)
    print(switch.cable(6))

switch_test()
