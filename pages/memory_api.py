# инициализация монитора памяти
# import psutil
# import os
import tracemalloc
from init.app_init import app

tracemalloc.start()
snap_old = tracemalloc.take_snapshot()
test = ['aboba']


# форматирует текст в табличный вид
def format_string(s: str) -> str:
    s = s.replace('<', '')
    s = s.replace('>', '')

    s = s.replace(': ', ', ').split(', ')

    s_ = s[0] + '&nbsp;'*(75-(len(s[0])))
    s.pop(0)
    for elem in s:
        elem = elem.strip()
        s_ += elem
        if elem != s[-1]:
            s_ += '&nbsp;'*(30-(len(elem)))
    return s_

#
# # посчитать, сколько мб весит процесс питона
# def count_all_weight():
#     process = psutil.Process()
#     weight = process.memory_info().rss
#     weight = weight / (1024*1024)
#     return int(weight)


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
    stat_list_plus = []
    stat_list_minus = []
    for stat in snap_new.compare_to(snap_old, 'lineno'):
        if not ('B (+0 B)' in str(stat) or 'bootstrap' in str(stat) or 'size=0' in str(stat)):
            stat = str(stat)
            if 'Autodiag_Delta' in stat:
                stat = stat.split('Autodiag_Delta')[-1]

            if 'B (+' in stat:
                stat_list_plus.append(format_string(stat))
            else:
                stat_list_minus.append(format_string(stat))

    return (
        '<code>' +
        # 'total process weight: ' + str(count_all_weight()) + ' Mb' + '<br>' +
        'mem addidions: ' + str(len(stat_list_plus)) + '<br>' +
        '<br>'.join(stat_list_plus) + '<br>' +
        '='*148 + '<br>' +
        'mem removes: ' + str(len(stat_list_minus)) + '<br>' +
        '<br>'.join(stat_list_minus) +
        '</code>'
    )
