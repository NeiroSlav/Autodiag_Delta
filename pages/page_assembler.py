from connections import switch_class
from connections import Tolerance, Telnet
from init import *


# вход на свитч, перенаправление на страницу свитча
@app.route("/", methods=["GET"])
def main_redirect():
    try:
        #  инициализация данных из GET запроса
        gcdb_data = GcdbData(request)  # парсинг GET запроса
        tolerance = Tolerance(gcdb_data)  # логин на tolerance
        switch_ip = gcdb_data.switch_ip

        if not tolerance.ping(switch_ip):  # если свитч не отвечает
            raise DiagError(f'Свитч {switch_ip} лежит')

        telnet = Telnet(gcdb_data)  # логин на свитч
        if not telnet.switch_type:  # если тип свитча не определён
            raise DiagError(f'Тип {switch_ip} не определён')

        if telnet.switch_type == 'DGS':
            raise DiagError(f'Это DGS, родной. Кыш отсюда')

        #  создание токена, сохранение данных, запись в сессию
        token = token_init()
        token_set(token, 'gcdb_data', gcdb_data)
        token_set(token, 'tolerance', tolerance)
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

        if telnet.switch_type != switch_type:  # редирект, если другой свитч
            return redirect(f'/{telnet.switch_type}/{token}')

        switch = switch_class[switch_type](telnet)  # сохраняет в токен объект свитча
        token_set(token, 'switch', switch)

        switch_info = f'{gcdb_data.switch_ip} : {gcdb_data.switch_port}'
        if gcdb_data.pon_port:
            switch_info += f' : {gcdb_data.pon_port}'

        return render_template(  # рендер страницы диагностики
            f'{switch_type}.html',
            topinfo=f'Вы на {switch_type.title()} {switch_info}',
            title=f'{switch_type.title()[0]} {switch_info}',
            token=token)

    except EOFError:  # если сессия telnet была разорвана
        return render_error('Сессия Telnet разорвана')

    except KeyError:  # если не нашлось токена
        return render_error(f'Токен {token} удалён')

    except Exception as ex:
        return render_error(ex)
