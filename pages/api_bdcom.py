from .page_assembler import *


# обработчик для диагностики порта
@app.route("/bdcom/get_port/<token>")
@use_token
def bdcom_get_port(token):
    port = token.gcdb_data.switch_port
    pon = token.gcdb_data.pon_port
    return token.switch.port(port, pon)


# обработчик для проверки мака
@app.route("/bdcom/get_mac/<token>")
@use_token
def bdcom_get_mac(token):
    port = token.gcdb_data.switch_port
    pon = token.gcdb_data.pon_port
    mac_list = token.gcdb_data.mac_list
    return token.switch.mac(port, pon, mac_list)


# обработчик для проверки сигнала
@app.route("/bdcom/get_signal/<token>")
@use_token
def bdcom_get_signal(token):
    port = token.gcdb_data.switch_port
    pon = token.gcdb_data.pon_port
    return token.switch.signal(port, pon)


# обработчик для проверки списка неактивных
@app.route("/bdcom/get_active/<token>")
@use_token
def bdcom_get_active(token):
    port = token.gcdb_data.switch_port
    pon = token.gcdb_data.pon_port
    return token.switch.active(port, pon)
