from init import *
from connections import Ubiquiti
from flask import redirect, request


# инициализация air-подключения в токене
@app.route("/air_init/<token_number>/", methods=["GET"])
def air_init(token_number):
    try:
        token = Token.pull(token_number)
        if not token:
            return render_error(f'Токен {token_number} удалён')

        base_ip = request.args.get('base_ip')
        station_ip = request.args.get('station_ip')
        if not base_ip or not station_ip:
            return render_error('Неполный запрос для air')

        air = Air()
        air.base = Ubiquiti(base_ip)
        if not air.base.connected:
            raise DiagError(f'База {base_ip} недоступна')

        air.station = Ubiquiti(station_ip)
        air.ip_list = [base_ip, station_ip]

        token.air = air
        return redirect(f'/air/{token}')
    # рендер страницы с ошибкой
    except Exception as ex:
        return render_error(ex)


# рендер страницы с air-подключением
@app.route("/air/<token_number>")
def air_page(token_number):
    token = Token.pull(token_number)

    try:
        if not token:
            return render_error(f'Токен {token_number} удалён')
        if not token.air:
            return render_error(f'Подключение air не объявлено в токене')

        base_ip = token.air.base.ip
        gcdb_data = token.gcdb_data

        return render_template(  # рендер страницы диагностики
            f'/air.html',
            anumber=gcdb_data.anumber,
            data=token.air,
            title=f'AIR {base_ip}',
            token=str(token),
            theme=user_sets.get(gcdb_data.username, 'theme'),
        )

    except Exception as ex:
        return render_error(ex)
