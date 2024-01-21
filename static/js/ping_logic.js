function setPingsDefault() {
    for (key in abonPingStatus) {
        abonPingStatus[key] = 'not started'
    }
    pingResultCache = {}
    pingResultDivCache = ' '
    pingResultTextCache = {}
    pingStarted = false
    pingNeed = false
}

var pingStarted = false
var pingNeed = false
var pingResultCache = {}
var pingResultDivCache = ' '
var pingResultTextCache = {}
var lastPingFlag = false


function updatePingProcess() {

    var need = false // проверяем, нужен ли кому-то пинг
    for (key in abonPingStatus) {
        if (abonPingStatus[key] == 'ping') {
            need = true
        }
    }

    if (need && !pingStarted) { // если пинг нужен, и не начат - начинаем
        console.log('starting ping')
        pingNeed = true
        pingStarted = true
        startPingProcess()
    }

    if (!need && pingStarted) { // если пинг идёт, но никому не нужен
        console.log('stopping ping')
        pingNeed = false
        lastPingFlag = true
        pingStarted = false
    }
}

// цикличный аякс, который вызывает сам себя каждые 0.2 секунды
// пока (панель открыта и (пинг кому-то нужен или это последний пакет))
function startPingProcess() {
    $.ajax({
        type: 'GET',
        url : '/iter_ping/' + token,
        dataType: 'json',
        data: {
            abonPingStatus : JSON.stringify(abonPingStatus)
            },
        success: function(response) {
            if (sidePanelShownFlag && (pingNeed || lastPingFlag)) {
                if (lastPingFlag) {lastPingFlag = false}
//                console.log(response)
                renderPingLog(response)
                renderPingResult(response)
                setTimeout( function() {startPingProcess()}, 200);
            }

        },
        error: function(error){
            if (sidePanelShownFlag && (pingNeed || lastPingFlag)) {
                if (lastPingFlag) {lastPingFlag = false}
                console.log('ping response has not came')
                setTimeout( function() {startPingProcess()}, 200);
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
            bMod['onclick'] = "abonPingStatus['" + ip + "'] = 'ping'; renderPingButtons();" +
                              "pingNeed = true; updatePingProcess();"
        }
        if (status == 'ping') {
            bMod['text'] = 'стоп'
            bMod['color'] = 'Red'
            bMod['onclick'] = "abonPingStatus['" + ip + "'] = 'finish'; renderPingButtons();" +
                              "updatePingProcess();"
        }
        if (status == 'finish') {
            bMod['text'] = 'ещё'
            bMod['color'] = 'Green'
            bMod['onclick'] = "abonPingStatus['" + ip + "'] = 'ping'; renderPingButtons();" +
                              "pingNeed = true; updatePingProcess();"
        }
        htmlText += getB(bIp) + getB(bMod)
    }
    var sidePingButtons = document.getElementById('sidePingButtons');
    sidePingButtons.innerHTML = htmlText
}


// обновление лога пинга
function renderPingLog(response) {

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

        if (data.ok) { // если пинг прошёл без потерь
            bRes['color'] = 'Green'
            bRes['text'] = 'пинг '+ ip + ' (' + data.sent + ')\n'
            bRes['text'] += 'lost:' + data.lost_percent + '% &nbsp;avg:' + data.stats.avg + ' &nbsp;max:' + data.stats.max

        } else if(data.lost == 100) { // если 100% потерь
            bRes['color'] = 'Red'
            bRes['text'] = 'пинг адреса '+ ip + '\n'
            bRes['text'] += 'не прошёл (пакетов: ' + data.sent + ')'

        } else { // если пинг прошёл, но были потери
            bRes['color'] = 'Red'
            bRes['text'] = 'пинг '+ ip + ' (' + data.sent + ')\n'
            bRes['text'] += 'lost:' + data.lost_percent + '% &nbsp;avg:' + data.stats.avg + ' &nbsp;max:' + data.stats.max
        }

        pingResultTextCache[ip] = bRes['text'].replace('&nbsp;', '(' + data.lost + '/' + data.sent + ') ').replace('&nbsp;', '')
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
