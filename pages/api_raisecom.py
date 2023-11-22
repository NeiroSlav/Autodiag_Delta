from .page_assembler import *


# обработчик для диагностики порта
@app.route("/raisecom/get_port/<token>")
@use_token
def raisecom_get_port(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.port(port)


# обработчик для выключения/включения порта
@app.route("/raisecom/disable_port/<token>")
@use_token
def raisecom_disable_port(token, **t_data):
    # забирает аргумент из запроса
    enable = request.args.get('enable') == 'true'
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    ip, port = gcdb_data.switch_ip, gcdb_data.switch_port
    # тут будет логирование данных
    print(f'{gcdb_data.username} {ip}:{port} ena:{enable}')
    return switch.set_port(port, enable=enable)


# обработчик для диагностики ошибок
@app.route("/raisecom/get_errors/<token>")
@use_token
def raisecom_get_errors(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.errors(port)


# обработчик для проверки мака
@app.route("/raisecom/get_mac/<token>")
@use_token
def raisecom_get_mac(token, **t_data):
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    port, mac_list = gcdb_data.switch_port, gcdb_data.mac_list
    result = switch.mac(port, mac_list)
    return result
