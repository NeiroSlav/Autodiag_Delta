from .app_init import *


# обработчик для проверки уд
@app.route("/get_open_port/<token>")
def get_open_port(token):
    if token_exists(token):
        gcdb_data = token_get(token, 'gcdb_data')
        tolerance = token_get(token, 'tolerance')
        return jsonify(tolerance.find_open_port(gcdb_data.abon_ip))  # возврат ответа в json
    return jsonify({'error': True, 'type': 'TokenNotFound'})  # ошибка, если токена нет
