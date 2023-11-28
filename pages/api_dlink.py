from .page_assembler import *


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

    log_string = f'{gcdb_data.username} {"enabled" if enable else "disabled"} {ip}:{port}'
    logging.warning(log_string)
    changes_list.append(log_string)

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
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    port, mac_list = gcdb_data.switch_port, gcdb_data.mac_list

    if token_get(token, 'first_time_flag'):
        if not switch.loose(port)['ok']:
            switch.set_bind(port, loose=True)
            token_changes(token, 'set_bind_loose')
            token_set(token, 'first_time_flag', False)

    result = switch.mac(port, mac_list)
    return result


# обработчик для проверки лога
@app.route("/dlink/get_log/<token>")
@use_token
def dlink_get_log(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.log(port)


# обработчик для проверки лога
@app.route("/dlink/get_full_log/<token>")
@use_token
def dlink_get_full_log(token, **t_data):
    switch = t_data['switch']
    return switch.log()


# обработчик для проверки трафика
@app.route("/dlink/get_util/<token>")
@use_token
def dlink_get_util(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.util(port)
