import threading
import time
import tracemalloc
import linecache
from pympler import muppy
from pympler import summary


tracemalloc.start()


def memory_display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def memory_watch_stats():
    while True:

        # command = input()
        time.sleep(10)
        command = 'sum'

        print(command)
        # try:
        #     arg = int(command.split()[1])
        # except:
        #     arg = 10

        print(' =' * 20)

        # if 'top' in command:
        #     print(f'[ top {arg} ]')
        #     snapshot = tracemalloc.take_snapshot()
        #     memory_display_top(snapshot, limit=arg)

        if 'sum' in command:
            all_objects = muppy.get_objects()
            sum1 = summary.summarize(all_objects)
            summary.print_(sum1, limit=7)

            del all_objects
            del sum1

        # if 'dif' in command:
        #     if snapshot1:
        #         snapshot2 = tracemalloc.take_snapshot()
        #         top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        #
        #         print("[ Top 10 differences ]")
        #         for stat in top_stats[:arg]:
        #             print(stat)
        #         snapshot1 = snapshot2
        #     else:
        #         snapshot1 = tracemalloc.take_snapshot()

        print(' =' * 20)


oom_thread = threading.Thread(target=memory_watch_stats)

if __name__ == '__main__':
    oom_thread.start()
