from .page_assembler import *


# обработчик для диагностики порта
@app.route("/zyxel/get_port/<token>")
@use_token
def zyxel_get_port(token):
    port = token.gcdb_data.switch_port
    return token.switch.port(port) | token.switch.enabled(port)


# обработчик для выключения/включения порта
@app.route("/zyxel/disable_port/<token>")
@use_token
def zyxel_disable_port(token):
    # забирает аргумент из запроса
    set_flag = bool(request.args.get('enable') == 'true')
    ip, port = token.gcdb_data.switch_ip, token.gcdb_data.switch_port
    username = token.gcdb_data.username

    log_string = f'{username} {"enabled" if set_flag else "disabled"} {ip}:{port}'
    logging.warning(log_string)
    Token.changes_list.append(log_string)

    return token.switch.set_port(port, enable=set_flag)


# обработчик для диагностики кабеля
@app.route("/zyxel/cable_diag/<token>")
@use_token
def zyxel_get_cable(token):
    port = token.gcdb_data.switch_port
    return token.switch.cable(port)


# обработчик для проверки мака
@app.route("/zyxel/get_mac/<token>")
@use_token
def zyxel_get_mac(token):
    port = token.gcdb_data.switch_port
    mac_list = token.gcdb_data.mac_list
    return token.switch.mac(port, mac_list)


# обработчик для проверки лога
@app.route("/zyxel/get_log/<token>")
@use_token
def zyxel_get_log(token):
    port = token.gcdb_data.switch_port
    return token.switch.log(port)


# обработчик для проверки лога
@app.route("/zyxel/get_full_log/<token>")
@use_token
def zyxel_get_full_log(token):
    return token.switch.log()
