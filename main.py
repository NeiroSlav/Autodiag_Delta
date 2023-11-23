from pages import *
from init.memory_watcher import oom_thread


if __name__ == '__main__':
    token_thread.start()
    # oom_thread.start()
    # app.run(debug=False, host='10.0.250.29', port=8000)  # мой впн
    app.run(debug=True, host='192.168.252.133', port=8000)  # ип сервера
