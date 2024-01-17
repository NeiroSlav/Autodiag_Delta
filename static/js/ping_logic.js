
var abonPingStatus = {
    '192.168.0.1': 'start',
    '124.123.12.1': 'start',
    '63.51.1.5': 'start',
    }

// цикличный аякс, который вызывает сам себя каждую секунду
// пока флаг открытой панели не станет false
function startPingProcess() {
    $.ajax({
        type: 'GET',
        url : '/iter_ping',
        dataType: 'json',
        data: {
            abonPingStatus : JSON.stringify(abonPingStatus)
            },
        success: function(response){
            if (sidePanelShownFlag) {
                console.log(response)
//                renderPingLog(response)
                setTimeout( function() {startPingProcess()}, 100);
            }
        },
        error: function(error){
            if (sidePanelShownFlag) {
                console.log('ping_response has not came')
                setTimeout( function() {startPingProcess()}, 100);
            }
        }
});}

// генерация, и рендеринг html текста кнопок для блока ип в пинге
function renderPingButtons(addStyle = 'opacity: 1') {

    bTitle = setB()
    bTitle['style'] = 'width: 220px;' + addStyle
    bTitle['text'] = 'Пинг абонентских IP:'
    bTitle['extra'] = 'sideElem'
    htmlText = getB(bTitle)

    for (const [key, value] of Object.entries(abonPingStatus)) {
        bIp = setB()
        bIp['style'] = 'width: 162px;' + addStyle
        bIp['text'] = key
        bIp['extra'] = 'sideElem'

        bMod = setB()
        bMod['style'] = 'width: 54px;' + addStyle
        bMod['extra'] = 'sideElem'

        if (value == 'start') {
            bMod['text'] = 'старт'
            bMod['color'] = 'Blue'
            bMod['onclick'] = "abonPingStatus['" + key +
                              "'] = 'ping'; renderPingButtons();"
        }
        if (value == 'ping') {
            bMod['text'] = 'стоп'
            bMod['color'] = 'Red'
            bMod['onclick'] = "abonPingStatus['" + key +
                              "'] = 'finish'; renderPingButtons();"
        }
        if (value == 'finish') {
            bMod['text'] = 'ещё'
            bMod['color'] = 'Green'
            bMod['onclick'] = "abonPingStatus['" + key +
                              "'] = 'ping'; renderPingButtons();"
        }

        htmlText += getB(bIp) + getB(bMod)
    }

    console.log(abonPingStatus)

    var sidePingButtons = document.getElementById('sidePingButtons');
    sidePingButtons.innerHTML = htmlText
}


//function renderPingLog(response) {
//    var diagLogBlock = ['<div class="diagLogBlock">','</div>']
//    var sidePingLogInnerDiv = document.getElementById('sidePingLogInner');
//
////    for (var elem in response.ok) {
//    log_elem = diagLogBlock[0] + response.ok + diagLogBlock[1]
//    sidePingLogInnerDiv.innerHTML += log_elem
////    }
//}