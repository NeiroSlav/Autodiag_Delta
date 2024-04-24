# import token

from flask import redirect, request

from connections import Telnet, fping
from init import *
from .page_assembler_utils import *
from .simple_page import render_simple_page


# вход на свитч, перенаправление на страницу свитча
@app.route("/", methods=["GET"])
def main_redirect():
    #  инициализация данных из GET запроса
    gcdb_data = GcdbData(request)  # парсинг GET запроса

    # если сотрудник из АО, для него грузится упрощённая страница
    if user_sets.get(gcdb_data.username, 'division') == 'ao':
        return render_simple_page(gcdb_data)

    switch_ip = gcdb_data.switch_ip
    switch_port = gcdb_data.switch_port

    session['theme'] = user_sets.get(gcdb_data.username, 'theme')

    try:
        if not fping(gcdb_data.switch_ip):  # если свитч не отвечает
            return render_switch_down(gcdb_data)  # отрисовка страницы с лежачим
        telnet = Telnet(switch_ip)  # логин на свитч
        validate_switch_access(telnet, switch_port)

        token = Token()  # создание токена,
        token.gcdb_data = gcdb_data  # сохранение данных
        token.telnet = telnet  # сохранение данных
        init_switch(token)  # создание объекта свитча

        if wrong_flats_page := find_wrong_flats(token):
            return wrong_flats_page

        # если тип свитча определён, и флаты ок - открыть его страницу
        return redirect(f'/{telnet.switch_type}/{token}')

    # рендер страницы с ошибкой
    except Exception as ex:
        return render_error(ex)


# рендер главной страницы свитча
@app.route("/<switch_type>/<token_number>")
def switch_page(switch_type, token_number):
    token = Token.pull(token_number)

    try:
        if not token:
            return render_error(f'Токен {token_number} удалён')
        telnet = token.telnet
        gcdb_data = token.gcdb_data
        gcdb_data.update_data()

        if telnet.switch_type != switch_type:  # редирект, если другой свитч
            return redirect(f'/{telnet.switch_type}/{token}')

        switch_info = f'{gcdb_data.switch_ip} : {gcdb_data.switch_port}'
        if gcdb_data.pon_port:
            switch_info += f' : {gcdb_data.pon_port}'

        return render_template(  # рендер страницы диагностики
            f'/switch/{switch_type}.html',
            switchtype=f'{switch_type.upper()} {token.switch.model}',
            title=f'{switch_type.title()[0]} {switch_info}',
            theme=user_sets.get(gcdb_data.username, 'theme'),
            topinfo=switch_info,
            token=str(token),
            data=gcdb_data,
        )

    except EOFError:  # если сессия telnet была разорвана
        token.delete()
        return render_error('Сессия Telnet разорвана')

    except Exception as ex:
        if token:
            token.delete()
        return render_error(ex)


# меняет тему оформления для юзера
@app.route("/change_theme/<token>")
def change_theme(token):
    token = Token.pull(token)
    if not token:
        return {'ok': False}

    username = token.gcdb_data.username
    current_theme = user_sets.get(username, 'theme')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    user_sets.set(username, 'theme', new_theme)
    return {'ok': True}


# принимает запрос на создание тикета
@app.route("/create_ticket")
def create_ticket():
    status = GcdbApi.set_ticket(
        request.args.get('anumber'),
        request.args.get('user'),
        request.args.get('ticket_id'),
        request.args.get('comment'),
    )
    return status
