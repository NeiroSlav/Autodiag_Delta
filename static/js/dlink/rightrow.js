function get_log_business (response) {

    var b1 = setB()
    b1['text'] = 'Только порт'
    b1['onclick'] = 'get_log();'
    b1['style'] = 'width: 116px;'
    b1['id'] = 'mainButton'

    var b3 = setB()
    b3['text'] = 'Весь лог'
    b3['onclick'] = 'get_full_log();'
    b3['style'] = 'width: 116px;'
    b3['id'] = 'mainButton2'


    var b2 = setB()
    b2['text'] = 'Штормов/колец не найдено'
    b2['style'] = 'width: 236px;'

    var diagLog = ['<div class="diagLog">','</div>']
    var diagLogLong = ['<div class="diagLog" style="height: 278px;">','</div>']
    var diagLogRed = ['<div class="diagLog" style="border-color: var(--error-color); height: 280px; background-color: var(--error-color)">','</div>']

    var diagSnmp = ['<div class="diagLog" style="height: 86px;">','</div>']
    var diagLogBlock = ['<div class="diagLogBlock">','</div>']

    if (response.error) {  // если вернулась ошибка
        b1['color'] = b2['color'] = 'Red'
        b2['text'] = 'ошибки они такие...'
        errMsg = diagLogBlock[0] + 'ошибка проверки лога' + diagLogBlock[1]
        return getB(b1) + getB(b3) + diagLogRed[0] + errMsg + diagLogRed[1] + getB(b2)
    } else {

        var all_logs = ''  // составление списка лога
        for (var elem in response.log) {
            log_elem = diagLogBlock[0] + response.log[elem] + diagLogBlock[1]
            all_logs = all_logs + log_elem
        }
        if (all_logs == '') { // если записей в логе нет
            all_logs = diagLogBlock[0] + 'Нет записей этого порта' + diagLogBlock[1]
        }

        var all_snmp = ''  // составление списка снмп
        for (var elem in response.snmp) {
        snmp_elem = diagLogBlock[0] + response.snmp[elem] + diagLogBlock[1]
        all_snmp = all_snmp + snmp_elem
        }

        if (response.ok) {  // если ок
            b1['color'] = b2['color'] = 'Green'

            return getB(b1) + getB(b3) + diagLogLong[0] + all_logs + diagLogLong[1] + getB(b2)

        } else {  // если не ок
            b1['color'] = 'Red'

            if (all_snmp == '') {  // если список штормов/колец пуст
                b2['color'] = 'Green'
                return getB(b1) + getB(b3) + diagLogLong[0] + all_logs + diagLogLong[1] + getB(b2)

            } else {  // если есть шторм/кольцо
                b2['color'] = 'Red'
                b2['text'] = 'Шторм/кольцо порта за 24ч:'
                return getB(b1) + getB(b3) + diagLog[0] + all_logs + diagLog[1] +
                       getB(b2) + diagSnmp[0] + all_snmp + diagSnmp[1]
            }
        }
    }}



function get_full_log_business (response) {

    var b1 = setB()
    b1['text'] = 'Только порт'
    b1['onclick'] = 'get_log();'
    b1['style'] = 'width: 116px;'
    b1['id'] = 'mainButton'

    var b3 = setB()
    b3['text'] = 'Весь лог'
    b3['onclick'] = 'get_full_log();'
    b3['style'] = 'width: 116px;'
    b3['id'] = 'mainButton2'

    var diagLogLong = ['<div class="diagLog" style="height: 310px;">','</div>']
    var diagLogBlock = ['<div class="diagLogBlock">','</div>']
    var diagLogRed = ['<div class="diagLog" style="border-color: var(--error-color); height: 312px; background-color: var(--error-color)">','</div>']


    if (response.error) {  // если вернулась ошибка
        b3['color'] = 'Red'
        errMsg = diagLogBlock[0] + 'ошибка проверки лога' + diagLogBlock[1]
        return getB(b1) + getB(b3) + diagLogRed[0] + errMsg + diagLogRed[1]
    } else {

        var all_logs = ''  // составление списка лога
        for (var elem in response.log) {
            log_elem = diagLogBlock[0] + response.log[elem] + diagLogBlock[1]
            all_logs = all_logs + log_elem
        }
        if (all_logs == '') { // если записей в логе нет
            all_logs = diagLogBlock[0] + 'Нет записей в логе' + diagLogBlock[1]
        }

        b3['color'] = 'Green'
        return getB(b1) + getB(b3) + diagLogLong[0] + all_logs + diagLogLong[1]

    }}