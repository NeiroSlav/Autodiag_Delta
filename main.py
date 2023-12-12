from pages import *


if __name__ == '__main__':
    token_thread.start()

    app.run(debug=True, port=8000)  # локалхост

    app.run(debug=False, host='192.168.252.133', port=8000)  # ип сервера
