from connections import switch_class
from connections import Telnet, fping, nmap
from init import *


@app.route("/test/<switch_type>/")
def test_page(switch_type):
    return render_template(  # рендер тестовой страницы
        f'{switch_type}.html',
        switchip='192.168.13.54',
        switchtype=switch_type.upper(),
        topinfo='192.168.13.54 : 12',
        title=f'D 192.168.13.54')


# вход на свитч, перенаправление на страницу свитча
@app.route("/", methods=["GET"])
def main_redirect():
    try:
        #  инициализация данных из GET запроса
        gcdb_data = GcdbData(request)  # парсинг GET запроса
        switch_ip = gcdb_data.switch_ip

        if not fping(switch_ip):  # если свитч не отвечает
            raise DiagError(f'Свитч {switch_ip} лежит')

        telnet = Telnet(gcdb_data)  # логин на свитч
        if not telnet.switch_type:  # если тип свитча не определён
            raise DiagError(f'Тип {switch_ip} не определён')

        if telnet.switch_type == 'DGS':
            raise DiagError(f'Это DGS, родной. Кыш отсюда')

        #  создание токена, сохранение данных, запись в сессию
        token = token_init()
        token_set(token, 'gcdb_data', gcdb_data)
        token_set(token, 'telnet', telnet)

        # если тип свитча определён, открыть его страницу
        return redirect(f'/{telnet.switch_type}/{token}')

    # рендер страницы с ошибкой
    except Exception as ex:
        return render_error(ex)


# рендер главной страницы свитча
@app.route("/<switch_type>/<token>")
def switch_page(switch_type, token):
    try:
        # распаковка данных из токена
        gcdb_data = token_get(token, 'gcdb_data')
        telnet = token_get(token, 'telnet')

        if switch_type == 'delete':  # удаляет токен
            token_del(token)
            raise DiagError(f'Вы удалили токен {token}')

        elif telnet.switch_type != switch_type:  # редирект, если другой свитч
            return redirect(f'/{telnet.switch_type}/{token}')

        switch = switch_class[switch_type](telnet)  # сохраняет в токен объект свитча
        token_set(token, 'switch', switch)

        switch_info = f'{gcdb_data.switch_ip} : {gcdb_data.switch_port}'
        if gcdb_data.pon_port:
            switch_info += f' : {gcdb_data.pon_port}'

        return render_template(  # рендер страницы диагностики
            f'{switch_type}.html',
            anumber=gcdb_data.anumber,
            switchip=gcdb_data.switch_ip,
            switchtype=switch_type.upper(),
            topinfo=f'{switch_type.title()} {switch_info}',
            title=f'{switch_type.title()[0]} {switch_info}',
            token=token)

    except EOFError:  # если сессия telnet была разорвана
        return render_error('Сессия Telnet разорвана')

    except KeyError:  # если не нашлось токена
        return render_error(f'Токен {token} удалён')

    except Exception as ex:
        return render_error(ex)
