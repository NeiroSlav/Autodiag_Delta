from .page_assembler import *


# обработчик для диагностики порта
@app.route("/bdcom/get_port/<token>")
@use_token
def bdcom_get_port(token, **t_data):
    switch = t_data['switch']
    port = t_data['gcdb_data'].switch_port
    pon = t_data['gcdb_data'].pon_port
    return switch.port(port, pon)


# обработчик для проверки мака
@app.route("/bdcom/get_mac/<token>")
@use_token
def bdcom_get_mac(token, **t_data):
    switch = t_data['switch']
    port = t_data['gcdb_data'].switch_port
    pon = t_data['gcdb_data'].pon_port
    return switch.mac(port, pon)


# обработчик для проверки сигнала
@app.route("/bdcom/get_signal/<token>")
@use_token
def bdcom_get_signal(token, **t_data):
    switch = t_data['switch']
    port = t_data['gcdb_data'].switch_port
    pon = t_data['gcdb_data'].pon_port
    return switch.signal(port, pon)


# обработчик для проверки списка неактивных
@app.route("/bdcom/get_active/<token>")
@use_token
def bdcom_get_active(token, **t_data):
    switch = t_data['switch']
    port = t_data['gcdb_data'].switch_port
    pon = t_data['gcdb_data'].pon_port
    return switch.active(port, pon)
