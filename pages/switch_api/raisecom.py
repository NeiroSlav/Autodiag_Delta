from pages.page_assembler import *


# обработчик для диагностики порта
@app.route("/raisecom/get_port/<token>")
@use_token
def raisecom_get_port(token):
    port = token.gcdb_data.switch_port
    return token.switch.port(port)


# обработчик для выключения/включения порта
@app.route("/raisecom/disable_port/<token>")
@use_token
def raisecom_disable_port(token):
    # забирает аргумент из запроса
    set_flag = bool(request.args.get('enable') == 'true')
    ip, port = token.gcdb_data.switch_ip, token.gcdb_data.switch_port
    username = token.gcdb_data.username

    log_string = f'{username} {"enabled" if set_flag else "disabled"} {ip}:{port}'
    logging.warning(log_string)
    Token.changes_list.append(log_string)

    return token.switch.set_port(port, enable=set_flag)


# обработчик для диагностики ошибок
@app.route("/raisecom/get_errors/<token>")
@use_token
def raisecom_get_errors(token):
    port = token.gcdb_data.switch_port
    return token.switch.errors(port)


# обработчик для проверки мака
@app.route("/raisecom/get_mac/<token>")
@use_token
def raisecom_get_mac(token):
    port = token.gcdb_data.switch_port
    mac_list = token.gcdb_data.mac_list
    return token.switch.mac(port, mac_list)
