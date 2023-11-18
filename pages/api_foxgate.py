from .page_assembler import *


# обработчик для диагностики порта
@app.route("/foxgate/get_port/<token>")
@use_token
def foxgate_get_port(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.port(port)


# обработчик для выключения/включения порта
@app.route("/foxgate/disable_port/<token>")
@use_token
def foxgate_disable_port(token, **t_data):
    # забирает аргумент из запроса
    enable = request.args.get('enable') == 'true'
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    ip, port = gcdb_data.switch_ip, gcdb_data.switch_port
    # тут будет логирование данных
    print(f'{gcdb_data.username} {ip}:{port} ena:{enable}')
    return switch.set_port(port, enable=enable)


# обработчик для проверки мака
@app.route("/foxgate/get_mac/<token>")
@use_token
def foxgate_get_mac(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    result = switch.mac(port)
    return result
