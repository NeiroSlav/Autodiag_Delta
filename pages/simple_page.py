from flask import render_template

from connections import Telnet, fping, _switch
from init import GcdbData
from .page_assembler_utils import render_switch_down


# простейшая диагностика для абонентского отдела
def render_simple_page(gcdb_data: GcdbData):
    switch_ip = gcdb_data.switch_ip
    port_data = {
        'port': gcdb_data.switch_port,
        'pon': gcdb_data.pon_port
    }

    if not fping(gcdb_data.switch_ip):  # если свитч не отвечает
        return render_switch_down(gcdb_data, simple=True)  # отрисовка страницы с лежачим

    telnet = Telnet(switch_ip)  # логин на свитч
    switch_type = telnet.switch_type

    #  если это медленный свитч, к нему доп параметры
    if 'DES-1210' in telnet.switch_model:
        telnet.x_timeout = 2
        switch_type = 'dlink1210'

    # прогон быстрой диагностики свитча
    switch = _switch[switch_type](telnet)
    diag_data: dict = switch.fast_check(port_data)

    # проверка диагностики на ошибки и корректность
    for key, elem in diag_data.items():

        # если есть ошибка диагностики
        if elem['error']:
            return render_template(
                'simple.html',
                topinfo=f'Ошибка во время диагностики: "{key}"',
                diag_error=True
            )

        # если какой-то параметр не ок
        if not elem['ok']:
            return render_template(
                'simple.html',
                topinfo=f'На линии есть проблемы: "{key}"',
                diag_error=True
            )

    # если в диагностике всё отлично
    return render_template(
        'simple.html',
        topinfo=f'Линия абонента в порядке, нарушений нет',
        diag_error=False
    )
