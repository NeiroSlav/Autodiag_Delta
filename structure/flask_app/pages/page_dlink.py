from .page_main import *


# обработчик для диагностики порта
@app.route("/dlink/get_port/<token>")
@use_token
def dlink_get_port(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.port(port)


# обработчик для выключения/включения порта
@app.route("/dlink/disable_port/<token>")
@use_token
def dlink_disable_port(token, **t_data):
    # забирает аргумент из запроса
    enable = request.args.get('enable') == 'true'
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    ip, port = gcdb_data.switch_ip, gcdb_data.switch_port
    # тут будет логирование данных
    print(f'{gcdb_data.username} {ip}:{port} ena:{enable}')
    return switch.set_port(port, enable=enable)


# обработчик для диагностики ошибок
@app.route("/dlink/get_errors/<token>")
@use_token
def dlink_get_errors(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.errors(port)


# обработчик для очистки ошибок
@app.route("/dlink/clear/<token>")
@use_token
def dlink_clear(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.clear(port)


# обработчик для диагностики кабеля
@app.route("/dlink/cable_diag/<token>")
@use_token
def dlink_get_cable(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.cable(port)


# обработчик для проверки привязки
@app.route("/dlink/get_bind/<token>")
@use_token
def dlink_get_bind(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.bind(port)


# обработчик для проверки мака
@app.route("/dlink/get_mac/<token>")
@use_token
def dlink_get_mac(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    result = switch.mac(port)
    result['loose'] = switch.loose(port)
    return result


# обработчик для проверки лога
@app.route("/dlink/get_log/<token>")
@use_token
def dlink_get_log(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.log(port)
