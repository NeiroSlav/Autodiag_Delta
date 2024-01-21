var pingResultCache = {}
var pingResultDivCache = ' '
var pingResultTextCache = {}

// цикличный аякс, который вызывает сам себя каждую секунду
// пока флаг открытой панели не станет false
function startPingProcess() {
    $.ajax({
        type: 'GET',
        url : '/iter_ping/' + token,
        dataType: 'json',
        data: {
            abonPingStatus : JSON.stringify(abonPingStatus)
            },
        success: function(response){
            if (sidePanelShownFlag) {
                console.log(response)
                renderPingLog(response)
                renderPingResult(response)
                setTimeout( function() {startPingProcess()}, 1000);
            }
        },
        error: function(error){
            if (sidePanelShownFlag) {
                console.log('ping_response has not came')
                setTimeout( function() {startPingProcess()}, 1000);
            }
        }
});}

// рендеринг html текста кнопок для блока ип в пинге
function renderPingButtons(addStyle = 'opacity: 1') {

    bTitle = setB()
    bTitle['style'] = 'width: 220px;' + addStyle
    bTitle['text'] = 'Пинг абонентских IP:'
    bTitle['extra'] = 'sideElem'
    var htmlText = getB(bTitle)

    for (const [ip, status] of Object.entries(abonPingStatus)) {
        bIp = setB()
        bIp['style'] = 'width: 162px;' + addStyle
        bIp['text'] = ip
        bIp['extra'] = 'sideElem'
        bIp['onclick'] = "saveClip('" + ip + "');"

        bMod = setB()
        bMod['style'] = 'width: 54px;' + addStyle
        bMod['extra'] = 'sideElem'

        if (status == 'not started') {
            bMod['text'] = 'старт'
            bMod['color'] = 'Blue'
            bMod['onclick'] = "abonPingStatus['" + ip +
                              "'] = 'ping'; renderPingButtons();"
        }
        if (status == 'ping') {
            bMod['text'] = 'стоп'
            bMod['color'] = 'Red'
            bMod['onclick'] = "abonPingStatus['" + ip +
                              "'] = 'finish'; renderPingButtons();"
        }
        if (status == 'finish') {
            bMod['text'] = 'ещё'
            bMod['color'] = 'Green'
            bMod['onclick'] = "abonPingStatus['" + ip +
                              "'] = 'ping'; renderPingButtons();"
        }

        htmlText += getB(bIp) + getB(bMod)
    }

    var sidePingButtons = document.getElementById('sidePingButtons');
    sidePingButtons.innerHTML = htmlText
}

// обновление лога пинга
function renderPingLog(response) {
    console.log(response)

    var sepBlock = '<div class="diagLogBlock"></div>'
    var okBlock = ['<div class="diagLogBlock" style="color: margin: 0 10px 0 10px;">','</div>']
    var lostBlock = ['<div class="diagLogBlock" style="color: margin: 0 10px 0 10px;">','</div>']

    var new_log_data = ''
    for (const [ip, data] of Object.entries(response.ping_data)) {
        if (data.ok) {
            console.log('ok')
            var diagLogBlock = okBlock
            var pingString = '&#9989;' + ip + ' пинг ' + data.answer + 'ms'
        } else {
            var diagLogBlock = lostBlock
            var pingString = '&#9940;' + ip + ' ответа нет'
        }
        new_log_data += diagLogBlock[0] + pingString + diagLogBlock[1]
    }
    if (new_log_data) {
        var sidePingLogInnerDiv = document.getElementById('sidePingLogInner');
        sidePingLogInnerDiv.innerHTML += sepBlock + new_log_data + sepBlock
        sidePingLogInnerDiv.scrollTop = sidePingLogInnerDiv.scrollHeight
    }
}



// генерация, и рендеринг html текста кнопок для блока ип в пинге
function renderPingResult(response) {

    for (const [ip, data] of Object.entries(response.ping_results)) {
        var bRes = setB()
        bRes['style'] = 'width: 220px; height: 45px; opacity: 1'
        bRes['extra'] = 'sideElem'

        if (data.ok) {
            bRes['color'] = 'Green'
            bRes['text'] = 'пинг '+ ip + ' (' + data.sent + ')\n'
            bRes['text'] += 'lost:' + data.lost + '% &nbsp;avg:' + data.stats.avg + ' &nbsp;max:' + data.stats.max

        } else if(data.lost == 100) {
            bRes['color'] = 'Red'
            bRes['text'] = 'пинг адреса '+ ip + '\n'
            bRes['text'] += 'не прошёл (пакетов: ' + data.sent + ')'

        } else {
            bRes['color'] = 'Red'
            bRes['text'] = 'пинг '+ ip + ' (' + data.sent + ')\n'
            bRes['text'] += 'lost:' + data.lost + '% &nbsp;avg:' + data.stats.avg + ' &nbsp;max:' + data.stats.max
        }

        pingResultTextCache[ip] = bRes['text'].replace('&nbsp;', '').replace('&nbsp;', '')
        bRes['onclick'] = "saveClip(pingResultTextCache['" + ip + "']);"

        pingResultCache[ip] = getB(bRes)

    }

    var htmlText = ''
    for (const [ip, buttonHtml] of Object.entries(pingResultCache)) {
        htmlText += buttonHtml
    }

    var sidePingResult = document.getElementById('sidePingResult');

    if (pingResultDivCache != htmlText) {
        sidePingResult.innerHTML = htmlText
        pingResultDivCache = htmlText;
    }
}