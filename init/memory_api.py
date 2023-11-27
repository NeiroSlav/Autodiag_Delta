# инициализация монитора памяти
import tracemalloc
from .app_init import app
tracemalloc.start()
snap_old = tracemalloc.take_snapshot()
test = ['aboba']


# обработчик для взятия первого слепка памяти
@app.route("/snap")
def set_mem():
    global snap_old
    snap_old = tracemalloc.take_snapshot()
    return 'взял базовый слепок'


# обработчик для взятия второго слепка памяти, и сравнения
@app.route("/compare")
def get_mem():
    snap_new = tracemalloc.take_snapshot()
    stat_list = []
    for stat in snap_new.compare_to(snap_old, 'lineno'):
        if not ('B (+0 B)' in str(stat) or 'bootstrap' in str(stat)):
            if 'Autodiag_Delta' in stat:
                stat = str(stat).split('Autodiag_Delta')[-1]
            stat_list.append(stat)

    return str(len(stat_list)) + '<br>'.join(sorted(stat_list))
