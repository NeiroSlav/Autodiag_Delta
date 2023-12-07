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
    enable = bool(request.args.get('enable') == 'true')
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

    # если это первая проверка мака
    if token_get(token, 'first_time_flag'):
        bind_state = switch.bind_state(port) | {'auto': True}
        token_set(token, 'default_bind_state', bind_state['state'])
        token_set(token, 'first_time_flag', False)

    # если привязка отключена, ставит флаг disabled
    if token_get(token, 'default_bind_state') == 'Disabled':
        return {'binding': {}, 'disabled': True, 'ok': True, 'error': False}

    return switch.bind(port) | {'disabled': False}


# обработчик для проверки мака
@app.route("/dlink/get_mac/<token>")
@use_token
def dlink_get_mac(token, **t_data):
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    port, mac_list = gcdb_data.switch_port, gcdb_data.mac_list

    # если изначально был strict, то проверяет
    bind_state = {'state': token_get(token, 'default_bind_state'), 'auto': True}
    if bind_state['state'] == 'Strict':
        bind_state = switch.bind_state(port) | {'auto': False}

    result = switch.mac(port, mac_list)
    return result | bind_state


# обработчик перевода в loose
@app.route("/dlink/set_bind/<token>")
@use_token
def dlink_set_bind(token, **t_data):
    # забирает аргумент из запроса
    loose = bool(request.args.get('loose') == 'true')
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    ip, port = gcdb_data.switch_ip, gcdb_data.switch_port

    # создаёт запись лога
    log_string = f'{gcdb_data.username} {"set loose" if loose else "set strict"} {ip}:{port}'
    logging.warning(log_string)
    changes_list.append(log_string)

    token_changes(token, 'set_bind_loose', remove=not bool(loose))
    return switch.set_bind(port, loose=loose)


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
    return switch.util(port) | switch.flood()
