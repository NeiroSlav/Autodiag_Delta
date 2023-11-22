from pages import *


if __name__ == '__main__':
    token_thread.start()
    # app.run(debug=False, host='10.0.250.29', port=8000)  # мой им впн
    app.run(debug=False, host='10.255.255.133', port=8000)  # ип сервера