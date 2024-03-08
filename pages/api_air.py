from .init_air_page import *


# обработчик для запроса данных базы
@app.route("/air/get_base/<token>")
@use_token
def air_get_base(token):
    st_ip = token.air.station.ip
    return token.air.base.get_wifi_info(st_ip)


# обработчик для запроса данных станции
@app.route("/air/get_station/<token>")
@use_token
def air_get_station(token):
    mac_list = token.gcdb_data.mac_list
    result = {
        'link': token.air.station.get_local_link(),
        'mac': token.air.station.get_local_mac(mac_list),
    }
    return result
