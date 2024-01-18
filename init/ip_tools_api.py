import json
import time
from pprint import pprint

from connections import nmap, IterPing
import requests
from .app_init import app
from .token_init import Token, jsonify
from flask import request
from random import randint


# обработчик для проверки уд
@app.route("/get_open_port/<token>")
def get_open_port(token):
    token = Token.pull(token)
    if not token:  # ошибка, если токена нет
        return jsonify({'error': True, 'type': 'TokenNotFound'})

    answer = nmap(token.gcdb_data.abon_ip)
    if not answer['port']:  # если открытый порт не найден
        return jsonify(answer)  # возврат ответа в json

    try:  # попытка запроса на http, если не удалось - https
        requests.get(f'http://{answer["ip"]}:{answer["port"]}/', timeout=1)
        return jsonify(answer | {'protocol': 'http'})
    except Exception:
        return jsonify(answer | {'protocol': 'https'})


# обработчик для пинга абонентских ip
@app.route("/iter_ping/<token>")
def iter_ping(token):
    answer = {
        'ping_data': {},
        'ping_results': {},
    }

    try:
        token = Token.pull(token)
        ping_status = request.args.get('abonPingStatus')
        ping_status = json.loads(ping_status)

        if not ping_status:
            return jsonify(answer)

        # перебирает словарь со статусами
        for ip, status in ping_status.items():
            print(ip, status)

            if status == 'ping':  # отправит пинг на объект
                if ip not in token.abon_ping_dict:
                    token.abon_ping_dict[ip] = IterPing(ip)
                answer['ping_data'][ip] = token.abon_ping_dict[ip].ping()

            if status == 'finish':  # заберёт данные пинга
                if ip in token.abon_ping_dict:
                    answer['ping_results'][ip] = token.abon_ping_dict[ip].get_result()
                    del token.abon_ping_dict[ip]

        return jsonify(answer)

    except Exception as ex:
        return jsonify(answer | {'error': ex})
