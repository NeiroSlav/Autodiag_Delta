from connections import nmap
import requests
from .app_init import app
from .token_init import Token, jsonify


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
