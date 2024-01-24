from .page_assembler import *


# обработчик для диагностики порта
@app.route("/bdcom_fe/get_port/<token>")
@use_token
def bdcom_fe_get_port(token):
    port = token.gcdb_data.switch_port
    return token.switch.port(port)


# обработчик для проверки мака
@app.route("/bdcom_fe/get_mac/<token>")
@use_token
def bdcom_fe_get_mac(token):
    port = token.gcdb_data.switch_port
    mac_list = token.gcdb_data.mac_list
    return token.switch.mac(port, mac_list)
