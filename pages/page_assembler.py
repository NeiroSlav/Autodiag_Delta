# import token

from connections import _switch
from connections import Telnet, fping, nmap
from flask import request, redirect
from init import *


# вход на свитч, перенаправление на страницу свитча
@app.route("/", methods=["GET"])
def main_redirect():
    #  инициализация данных из GET запроса
    gcdb_data = GcdbData(request)  # парсинг GET запроса
    switch_ip = gcdb_data.switch_ip

    session['theme'] = user_sets.get(gcdb_data.username, 'theme')

    try:
        if not fping(switch_ip):  # если свитч не отвечает
            decview_info = DecviewApi.get_status(switch_ip)

            return render_template(
                'switch_down.html',
                topinfo=decview_info['state'],
                switch_log=decview_info['log'],
                anumber=gcdb_data.anumber,
                user=gcdb_data.username,
                group_tickets=gcdb_data.group_tickets,
                theme=session['theme']
            )

        telnet = Telnet(gcdb_data)  # логин на свитч
        if not telnet.switch_type:  # если тип свитча не определён
            raise DiagError(f'Тип {switch_ip} не определён')

        if telnet.switch_type == 'DGS':
            raise DiagError(f'Гигабитный свитч, доступ запрещён')

        if telnet.switch_type == 'dlink':
            ports = int(telnet.switch_model[-2] + telnet.switch_model[-1])
            allowed_ports = 24 if ports > 24 else (ports - 2)
            if int(gcdb_data.switch_port) > allowed_ports:
                raise DiagError(f'Гигабитный порт, доступ запрещён')

        #  создание токена, сохранение данных, запись в сессию
        token = Token()
        token.gcdb_data = gcdb_data
        token.telnet = telnet

        # если тип свитча определён, открыть его страницу
        return redirect(f'/{telnet.switch_type}/{token}')

    # рендер страницы с ошибкой
    except Exception as ex:
        return render_error(ex, gcdb_data.username)


# рендер главной страницы свитча
@app.route("/<switch_type>/<token_number>")
def switch_page(switch_type, token_number):
    token = Token.pull(token_number)

    try:
        if not token:
            render_error(f'Токен {token_number} удалён')
        telnet = token.telnet
        gcdb_data = token.gcdb_data
        gcdb_data.update_data()

        if telnet.switch_type != switch_type:  # редирект, если другой свитч
            return redirect(f'/{telnet.switch_type}/{token}')

        #  если это медленный свитч, к нему доп параметры
        if 'DES-1210' in telnet.switch_model:
            telnet.x_timeout = 2
            token.switch = _switch['dlink1210'](telnet)
        else:
            token.switch = _switch[switch_type](telnet)  # сохраняет в токен объект свитча

        switch_info = f'{gcdb_data.switch_ip} : {gcdb_data.switch_port}'
        if gcdb_data.pon_port:
            switch_info += f' : {gcdb_data.pon_port}'

        return render_template(  # рендер страницы диагностики
            f'/switch/{switch_type}.html',
            anumber=gcdb_data.anumber,
            switchip=gcdb_data.switch_ip,
            switchtype=f'{switch_type.upper()} {token.switch.model}',
            topinfo=switch_info,
            title=f'{switch_type.title()[0]} {switch_info}',
            token=str(token),
            theme=user_sets.get(gcdb_data.username, 'theme')
        )

    except EOFError:  # если сессия telnet была разорвана
        token.delete()
        return render_error('Сессия Telnet разорвана')

    except KeyError:  # если не нашлось токена
        return render_error(f'Токен {token_number} удалён')

    except Exception as ex:
        if token:
            token.delete()
        return render_error(ex)


# меняет тему оформления для юзера
@app.route("/change_theme/<token>")
def change_theme(token):
    username = Token.pull(token).gcdb_data.username
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
    print('ticket created')
    return {'ok': status}
