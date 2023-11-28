from ip_tools import ping
# from connections.telnet import Telnet
# from connections.switches.dlink import Dlink
# from personal_data import switch_login, switch_password
#
#
# class GcdbData:
#     switch_login = switch_login
#     switch_password = switch_password
#     switch_ip = '192.168.48.173'
#     switch_port = 20
#
#
# data = GcdbData()
#
# session = Telnet(data)
# switch = Dlink(session)
#
# # print(switch.set_port(GcdbData.switch_port, True))
# # print(switch.test_all(GcdbData.switch_port))
# while True:
#     print(switch.util(GcdbData.switch_port))


response = os.system("ping ya.ru")

print(ping('ya.ru'))