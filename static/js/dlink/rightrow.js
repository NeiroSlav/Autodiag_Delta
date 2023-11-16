function get_log_business (response) {

    var b1 = setB()
    b1['text'] = 'Записи порта в логе за 24ч:'
    b1['onclick'] = 'get_log();'
    b1['style'] = 'width: 236px;'
    b1['id'] = 'mainButton'

    var b2 = setB()
    b2['text'] = 'Штормов/колец не найдено'
    b2['onclick'] = 'get_log();'
    b2['style'] = 'width: 236px;'

    var diagLog = ['<div class="diagLog">','</div>']
    var diagLogLong = ['<div class="diagLog" style="height: 280px;">','</div>']
    var diagLogRed = ['<div class="diagLog" style="border: 2px solid #FF8855; height: 200px;">','</div>']

    var diagSnmp = ['<div class="diagLog" style="height: 88px;">','</div>']
    var diagLogBlock = ['<div class="diagLogBlock">','</div>']

    if (response.error) {  // если вернулась ошибка
        b1['color'] = b2['color'] = 'Red'
        b2['text'] = 'ошибки они такие...'
        errMsg = diagLogBlock[0] + 'ошибка проверки лога' + diagLogBlock[1]
        return getB(b1) + diagLogRed[0] + errMsg + diagLogRed[1] + getB(b2)
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

            if (response.log.length < 5) {
                return getB(b1) + diagLog[0] + all_logs + diagLog[1] + getB(b2)
            } else {
                return getB(b1) + diagLogLong[0] + all_logs + diagLogLong[1] + getB(b2)
            }

        } else {  // если не ок
            b1['color'] = 'Red'

            if (all_snmp == '') {  // если список штормов/колец пуст
                b2['color'] = 'Green'
                return getB(b1) + diagLogLong[0] + all_logs + diagLogLong[1] + getB(b2)

            } else {  // если есть шторм/кольцо
                b2['color'] = 'Red'
                b2['text'] = 'Шторм/кольцо порта за 24ч:'
                return getB(b1) + diagLog[0] + all_logs + diagLog[1] +
                       getB(b2) + diagSnmp[0] + all_snmp + diagSnmp[1]
            }
        }
    }}