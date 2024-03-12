function get_base_business(response) {

    var bInfo = setB() // кнопка "информация с базы:"
    bInfo['text'] = 'База:'
    bInfo['color'] = 'Green'
    bInfo['onclick'] = 'get_base();'
    bInfo['id'] = 'mainButton'

    var bIp = setB() // кнопка с ип базы
    bIp['text'] = base_ip
    bIp['style'] = 'width: 176px;'
    bIp['onclick'] = "saveClip('"+base_ip+"');"

    var bName = setB() // кнопка с именем базы
    bName['text'] = response.hostname
    bName['style'] = 'width: 236px; margin-bottom: 32px;'
    bName['onclick'] = "saveClip('"+response.hostname+"');"

    if (response.error) {
        bInfo['color'] = bIp['color'] = bName['color'] = 'Red'
        var bError = setB()
        bError['color'] = 'Red'
        bError['text'] = 'Ошибка запроса'
        bError['style'] = 'width: 236px; height: 220px;'
        return getB(bInfo) + getB(bIp) + getB(bName) + getB(bError);
    } else {
        var topButtons = getB(bInfo) + getB(bIp) + getB(bName)

        var diagData = '! Сигнал плохой:\n'
        if (response.ok) {
            diagData = '+ Сигнал хороший:\n'
        }
        diagData += gap + 'ур. шума: ' + response.noise + '\n'
        diagData += gap + 'ур. сигнал: ' + response.signal + '\n'
        updateDiagDict('signal', diagData)

        var bNoise = setB()
        bNoise['text'] = 'Уровень шума: ' + response.noise
        bNoise['style'] = 'width: 236px;'

        var bSignal = setB()
        bSignal['text'] = 'Сила сигнала: ' + response.signal
        bSignal['style'] = 'width: 236px; margin-bottom: 32px;'
        bNoise['onclick'] = bSignal['onclick'] = "copyDiag('signal')"

        if (response.ok) {
            bNoise['color'] = bSignal['color'] = 'Green'
        } else {
            bNoise['color'] = bSignal['color'] = 'Red'
        }
        var signalButtons = getB(bNoise) + getB(bSignal)


        var bPktInfo = setB()
        bPktInfo['style'] = 'width: 236px;'
        bPktInfo['text'] = 'Трафик между точками:'
        var bRx = setB()
        var bTx = setB()
        bRx['style'] = bTx['style'] = 'width: 116px;'
        bRx['text'] = 'in: ' + response.pkt_rx + ' Pkt/s'
        bTx['text'] = 'out: ' + response.pkt_tx + ' Pkt/s'
        pktButtons = getB(bPktInfo) + getB(bRx) + getB(bTx)

        var diagData = 'Время соединения:\n'
        diagData += gap + response.uptime + '\n'
        updateDiagDict('uptime', diagData)

        var bUptimeText = setB()
        var bUptime = setB()
        bUptimeText['text'] = 'Время соединения:'
        bUptime['text'] = response.uptime
        bUptime['style'] = bUptimeText['style'] = 'width: 236px;'

        bUptimeText['onclick'] = bUptime['onclick'] = "copyDiag('uptime')"
        uptimeButtons = getB(bUptimeText) + getB(bUptime)

    }

    return topButtons + signalButtons + pktButtons + uptimeButtons;
}
