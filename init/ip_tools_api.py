from .app_init import *
from connections import nmap
import requests


# обработчик для проверки уд
@app.route("/get_open_port/<token>")
def get_open_port(token):
    if not token_exists(token):  # ошибка, если токена нет
        return jsonify({'error': True, 'type': 'TokenNotFound'})

    gcdb_data = token_get(token, 'gcdb_data')
    answer = nmap(gcdb_data.abon_ip)
    if not answer['port']:  # если открытый порт не найден
        return jsonify(answer)  # возврат ответа в json

    try:  # попытка запроса на https, если не удалось - http
        requests.get(f'https://{answer["ip"]}/', timeout=1)
        return jsonify(answer | {'protocol': 'https'})
    except Exception:
        return jsonify(answer | {'protocol': 'http'})
