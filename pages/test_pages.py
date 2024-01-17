from init import *
from flask import request


@app.route("/test/theme/<theme>")
def test_theme(theme):
    return render_template(
        'test.html',
        theme=theme,
        topinfo='TEST TEST TEST',
    )


@app.route("/test/ping")
def test_ping():
    print('pinged')
    time.sleep(0.1)
    return jsonify({'ok': randint(0, 1000)})


@app.route("/iter_ping")
def iter_ping():
    ping_status = request.args.get('abonPingStatus')
    # print(ping_status)
    print('pinged')
    time.sleep(2)
    return jsonify(
        {'ok': f'lost: 0% avg: 30ms max: {randint(0, 1000)}ms'}
    )


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


@app.route("/test/<switch_type>")
def test_switch(switch_type):
    return render_template(  # рендер тестовой страницы
        f'/switch/{switch_type}.html',
        switchip='192.168.TE.ST',
        switchtype=switch_type.upper(),
        topinfo='192.168.TE.ST : XX',
        title=f'T 192.168.TE.ST',
        theme='dark'
    )


# меняет тему оформления для юзера
@app.route("/settings/<user>/set_theme/<theme>")
def settings_theme(user, theme):
    session['theme'] = theme
    user_sets.set(user, 'theme', theme)
    return {'ok': True}
