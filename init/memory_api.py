# инициализация монитора памяти
import tracemalloc
from .app_init import app
tracemalloc.start()
snap_old = tracemalloc.take_snapshot()
test = ['aboba']


# форматирует текст в табличный вид
def format_string(s: str) -> str:
    s = s.replace('<', '')
    s = s.replace('>', '')

    s = s.replace(': ', ', ').split(', ')

    s_ = s[0] + '&nbsp;'*(95-(len(s[0])))
    s.pop(0)
    for elem in s:
        elem = elem.strip()
        s_ += elem
        if elem != s[-1]:
            s_ += '&nbsp;'*(30-(len(elem)))
    return s_


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
            stat = str(stat)
            if 'Autodiag_Delta' in stat:
                stat = stat.split('Autodiag_Delta')[-1]
            stat_list.append(format_string(stat))

    return ('<code>' +
            'mem changes: ' + str(len(stat_list)) + '<br>' +
            '<br>'.join((stat_list)) + '</code>')
