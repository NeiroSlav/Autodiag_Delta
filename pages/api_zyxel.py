from .page_assembler import*


# обработчик для диагностики порта
@app.route("/zyxel/get_port/<token>")
@use_token
def zyxel_get_port(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.port(port)


# обработчик для выключения/включения порта
@app.route("/zyxel/disable_port/<token>")
@use_token
def zyxel_disable_port(token, **t_data):
    # забирает аргумент из запроса
    enable = request.args.get('enable') == 'true'
    switch, gcdb_data = t_data['switch'], t_data['gcdb_data']
    ip, port = gcdb_data.switch_ip, gcdb_data.switch_port
    # тут будет логирование данных
    print(f'{gcdb_data.username} {ip}:{port} ena:{enable}')
    return switch.set_port(port, enable=enable)


# обработчик для диагностики кабеля
@app.route("/zyxel/cable_diag/<token>")
@use_token
def zyxel_get_cable(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.cable(port)


# обработчик для проверки мака
@app.route("/zyxel/get_mac/<token>")
@use_token
def zyxel_get_mac(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    result = switch.mac(port)
    return result


# обработчик для проверки лога
@app.route("/zyxel/get_log/<token>")
@use_token
def zyxel_get_log(token, **t_data):
    switch, port = t_data['switch'], t_data['gcdb_data'].switch_port
    return switch.log(port)
