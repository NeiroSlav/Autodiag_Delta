from connections import Telnet
from init import dhcp_unity
from init import DiagError
from init.requests_out import DecviewApi
from flask.app import session
from flask import render_template
from connections import _switch


#  валидация доступа к свитчу
def validate_switch_access(telnet: Telnet, switch_port: int):

    if not telnet.switch_type:  # если тип свитча не определён
        raise DiagError(f'Тип {telnet.switch_ip} не определён')

    if telnet.switch_type == 'DGS':
        raise DiagError(f'Гигабитный свитч, доступ запрещён')

    if telnet.switch_type == 'dlink':
        ports = int(telnet.switch_model[-2] + telnet.switch_model[-1])
        allowed_ports = 24 if ports > 24 else (ports - 2)
        if int(switch_port) > allowed_ports:
            raise DiagError(f'Гигабитный порт, доступ запрещён')


#  рендеринг ошибки лежачего свитча
def render_switch_down(gcdb_data, simple: bool = False):

    decview_info = DecviewApi.get_status(gcdb_data.switch_ip)

    if simple:
        return render_template(
            'simple.html',
            topinfo=decview_info['state'],
            theme='light',
            diag_error=True
        )

    return render_template(
        'switch_down.html',
        topinfo=decview_info['state'],
        switch_log=decview_info['log'],
        abon_login=gcdb_data.abon_login,
        anumber=gcdb_data.anumber,
        phone=gcdb_data.phone,
        user=gcdb_data.username,
        group_tickets=gcdb_data.group_tickets,
        theme=session['theme']
    )


#  проверяет, есть ли неправильные флаты
def find_wrong_flat(token):
    try:
        return dhcp_unity.check_wrong_flat(token.gcdb_data.mac_list[0])
    except Exception:
        return


def render_wrong_flat_page(token, wrong_flat):
    return render_template(
        'wrong_flat.html',
        continue_link=f'/{token.telnet.switch_type}/{token}',
        flat_info=wrong_flat,
        anumber=token.gcdb_data.anumber,
        theme='dark',
    )


def init_switch(token):
    switch_type = token.telnet.switch_type

    #  если это медленный свитч, к нему доп параметры
    if 'DES-1210' in token.telnet.switch_model:
        token.telnet.x_timeout = 2
        switch_type = 'dlink1210'

    # сохраняет в токен объект свитча
    token.switch = _switch[switch_type](token.telnet)
