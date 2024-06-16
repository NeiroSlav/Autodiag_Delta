from init import *


@app.route("/test/theme/<theme>")
def test_theme(theme):
    return render_template(
        'test.html',
        theme=theme,
        topinfo='TEST TEST TEST',
    )


@app.route("/test/air")
def test_air():
    return render_template(
        '/air.html',
        theme='dark',
        topinfo='air_test_top',
    )


@app.route("/test/ping")
def test_ping():
    print('pinged')
    time.sleep(0.1)
    return jsonify({'ok': randint(0, 1000)})


@app.route("/test/down/<group>")
def test_down(group):
    group_name = 'Листопрокатчиков ул. 3А'
    group_dict = {}
    for i in range(int(group)):
        group_dict[f'000000{i+1}'] = f'{group_name} {i+1}'

    return render_template(
        'switch_down.html',
        topinfo='Свитч такой-то-там лежит с того-то того-то',
        switch_log=['2024-01-11 19:05:14 поднялся',
                    '2023-12-27 20:02:26 работает',
                    '2023-12-27 17:46:35 упал',
                    '2023-12-27 17:42:27 поднялся',
                    '2023-11-16 20:03:51 работает',
                    '2023-11-16 07:39:18 упал',
                    '2023-11-16 07:09:31 поднялся',
                    '2023-11-15 01:59:28 упал',
                    '2023-11-12 13:35:03 поднялся',
                    '2023-08-13 20:10:51 работает'],
        anumber='0000000000',
        user='bibus_bobus',
        group_tickets=group_dict,
        theme='dark'
    )


# пустой датакласс для тестов
class TestDataClass:
    pass


# тестовый рендер страницы для отладки css/html
@app.route("/test/<switch_type>")
def test_switch(switch_type):
    data = TestDataClass()
    data.ip_list = ['123.45.67.8']
    data.anumber = '1234567890'
    data.switch_ip = '123.45.67.8'

    return render_template(  # рендер тестовой страницы
        f'/switch/{switch_type}.html',
        switchtype=switch_type.upper(),
        topinfo='192.168.TE.ST : XX',
        title=f'T 192.168.TE.ST',
        theme='dark',
        data=data
    )


# меняет тему оформления для юзера
@app.route("/settings/<user>/set_theme/<theme>")
def settings_theme(user, theme):
    session['theme'] = theme
    user_sets.set(user, 'theme', theme)
    return {'ok': True}
