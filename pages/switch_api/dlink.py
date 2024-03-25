from pages.page_assembler import *


# обработчик для диагностики порта
@app.route("/dlink/get_port/<token>")
@use_token
def dlink_get_port(token):
    port = token.gcdb_data.switch_port
    return token.switch.port(port)


# обработчик для выключения/включения порта
@app.route("/dlink/disable_port/<token>")
@use_token
def dlink_disable_port(token):
    # забирает аргумент из запроса
    set_flag = bool(request.args.get('enable') == 'true')
    ip, port = token.gcdb_data.switch_ip, token.gcdb_data.switch_port
    username = token.gcdb_data.username

    log_string = f'{username} {"enabled" if set_flag else "disabled"} {ip}:{port}'
    logging.warning(log_string)
    Token.changes_list.append(log_string)

    return token.switch.set_port(port, enable=set_flag)


# обработчик для диагностики ошибок
@app.route("/dlink/get_errors/<token>")
@use_token
def dlink_get_errors(token):
    port = token.gcdb_data.switch_port
    return token.switch.errors(port)


# обработчик для очистки ошибок
@app.route("/dlink/clear/<token>")
@use_token
def dlink_clear(token):
    port = token.gcdb_data.switch_port
    return token.switch.clear(port)


# обработчик для диагностики кабеля
@app.route("/dlink/cable_diag/<token>")
@use_token
def dlink_get_cable(token):
    port = token.gcdb_data.switch_port
    return token.switch.cable(port)


# обработчик для проверки привязки
@app.route("/dlink/get_bind/<token>")
@use_token
def dlink_get_bind(token):
    port = token.gcdb_data.switch_port

    # если это первая проверка мака
    if token.first_time_flag:
        bind_state = token.switch.bind_state(port) | {'auto': True}
        token.default_bind_state = bind_state['state']
        token.first_time_flag = False

    # если привязка отключена, ставит флаг disabled
    if token.default_bind_state == 'Disabled':
        return {'binding': {}, 'disabled': True, 'ok': True, 'error': False}

    return token.switch.bind(port) | {'disabled': False}


# обработчик для проверки мака
@app.route("/dlink/get_mac/<token>")
@use_token
def dlink_get_mac(token):
    port = token.gcdb_data.switch_port
    mac_list = token.gcdb_data.mac_list

    # если изначально был strict, то проверяет
    bind_state = {'state': token.default_bind_state, 'auto': True}
    if bind_state['state'] == 'Strict':
        bind_state = token.switch.bind_state(port) | {'auto': False}

    result = token.switch.mac(port, mac_list)
    return result | bind_state


# обработчик перевода в loose
@app.route("/dlink/set_bind/<token>")
@use_token
def dlink_set_bind(token):
    # забирает аргумент из запроса
    loose_flag = bool(request.args.get('loose') == 'true')

    ip = token.gcdb_data.switch_ip
    port = token.gcdb_data.switch_port
    username = token.gcdb_data.username

    # создаёт запись лога
    log_string = f'{username} {"set loose" if loose_flag else "set strict"} {ip}:{port}'
    logging.warning(log_string)
    Token.changes_list.append(log_string)
    token.change('set_bind_loose', loose_flag)

    return token.switch.set_bind(port, loose=loose_flag)


# обработчик для проверки лога
@app.route("/dlink/get_log/<token>")
@use_token
def dlink_get_log(token):
    port = token.gcdb_data.switch_port
    return token.switch.log(port)


# обработчик для проверки лога
@app.route("/dlink/get_full_log/<token>")
@use_token
def dlink_get_full_log(token):
    return token.switch.log()


# обработчик для проверки трафика
@app.route("/dlink/get_util/<token>")
@use_token
def dlink_get_util(token):
    port = token.gcdb_data.switch_port
    if not token.gcdb_data.vlan:
        token.gcdb_data.vlan = token.switch.vlan(port)

    answer = {
        'util': token.switch.util(port),
        'igmp': token.switch.igmp(port),
        'flood': token.switch.flood(),
        'vlan': token.gcdb_data.vlan,
    }

    return answer
