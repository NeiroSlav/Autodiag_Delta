function hide (elements) {
//  elements = elements.length ? elements : [elements];
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.width = '0px';
    elements[i].style.opacity = '0';
    elements[i].textContent = '';
  }
}

function show (elements) {
//  elements = elements.length ? elements : [elements];
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.opacity = '1';
  }
}

var sidePanelShownFlag = false

function showSidePanel() {
    var sidePanel = document.getElementById('sidePanel');  // Достаём div
    var sepRight = document.getElementById('sepRight');
    var mainPanel = document.getElementById('mainPanel');

    if (sidePanelShownFlag) { //  если панель показана, то скрыть
        sidePanel.style.width = 0;
        sepRight.style.width = 0;
        mainPanel.style.padding = "0 48px 0 48px";

        var sideElems = document.querySelectorAll('.sideElem')
        hide(sideElems);

        var sidePingButtons = document.getElementById('sidePingButtons');
        var sidePingLog = document.getElementById('sidePingLog');
        var sidePingResult = document.getElementById('sidePingResult');

        setTimeout(function() {sidePingButtons.innerHTML = ''}, 150);
        setTimeout(function() {sidePingLog.innerHTML = ''}, 150);
        setTimeout(function() {sidePingResult.innerHTML = ''}, 150);

        for (key in abonPingStatus) {
            abonPingStatus[key] = 'not started'
        }
        pingResultCache = {}
        pingResultDivCache = ' '
        pingResultTextCache = {}


    } else {                 //  если панель скрыта, то показать
        sidePanel.style.width = 272 + "px";
        sepRight.style.width = 24 + "px";
        mainPanel.style.padding = "0 12px 0 12px";

        setTimeout(function() {
            renderPingButtons('');
            var sidePingLog = document.getElementById('sidePingLog');
            sidePingLog.innerHTML = '<div class="diagLog sideElem" id="sidePingLogInner" style="width: 216px;"> </div>'
        }, 500);
        setTimeout(function() {show(document.querySelectorAll('.sideElem'));}, 550);
        setTimeout(function() {startPingProcess();}, 600);
    }

    sidePanelShownFlag = !sidePanelShownFlag
}