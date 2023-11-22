from pages import *


if __name__ == '__main__':
    token_thread.start()
    # app.run(debug=False, host='10.0.250.29', port=8000)  # мой им впн
    # app.run(debug=False, host='192.168.252.133', port=8000)  # ип сервера
    app.run(debug=True, host='192.168.252.133', port=8000)  # ип сервера