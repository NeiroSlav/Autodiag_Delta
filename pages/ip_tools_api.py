import json

from connections import nmap, IterPing
from init.app_init import app
from init.token_init import Token, jsonify
from flask import request


# обработчик для проверки уд
@app.route("/get_open_port/<token>")
def get_open_port(token):
    token = Token.pull(token)
    if not token:  # ошибка, если токена нет
        return jsonify({'error': True, 'type': 'TokenNotFound'})

    return jsonify(nmap(token.gcdb_data.abon_ip))


# обработчик для пинга абонентских ip
@app.route("/iter_ping/<token>")
def iter_ping(token):
    answer = {
        'ping_data': {},
        'ping_results': {},
    }

    token = Token.pull(token)
    if not token:
        return {'error': 'Token Not Found'}

    ping_status = request.args.get('abonPingStatus')
    ping_status = json.loads(ping_status)

    if not ping_status:
        return jsonify(answer)

    # перебирает словарь со статусами
    for ip, status in ping_status.items():

        if status == 'ping':  # отправит пинг на объект
            if ip not in token.abon_ping_dict:
                token.abon_ping_dict[ip] = IterPing(ip)
            answer['ping_data'][ip] = token.abon_ping_dict[ip].ping()

        if status == 'finish':  # заберёт данные пинга
            if ip in token.abon_ping_dict:
                answer['ping_results'][ip] = token.abon_ping_dict[ip].get_result()
                del token.abon_ping_dict[ip]

    return jsonify(answer)
