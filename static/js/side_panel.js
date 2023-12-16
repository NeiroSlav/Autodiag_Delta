var getSideHtml = '' +
                '<div class="diagLongBlock">' +
                    '<div style="margin-bottom: 40px;"></div>' +
                    '<div class="diagMiniBlock">' +
                        '<div class="diagLog"></div>' +
                        '<button class="diagButtonRed">obabok</button>' +
                    '</div>' +
            '</div>'

function hide (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.transition = '0.4s';
    elements[index].style.width = '0';
    elements[index].style.opacity = '0';
    elements[index].style.width = '';

    elements[index].textContent = '';
  }
}

function show (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.transition = '';
    elements[index].style.width = '222px';
    elements[index].style.opacity = '1';

  }
}

var sidePanelShownFlag = false

function showSidePanel() {
    var sidePanel = document.getElementById('sidePanel');  // Достаём div
    var sepRight = document.getElementById('sepRight');
    var mainPanel = document.getElementById('mainPanel');

    var button1 = document.getElementById('sideButton');


    if (sidePanelShownFlag) { //  если панель показана, то скрыть
        sidePanel.style.width = 0;
        sepRight.style.width = 0;
        mainPanel.style.padding = "0 48px 0 48px";

        hide(document.querySelectorAll('.sideElem'));


    } else {                 //  если панель скрыта, то показать
        sidePanel.style.width = 272 + "px";
        sepRight.style.width = 24 + "px";
        mainPanel.style.padding = "0 12px 0 12px";

        show(document.querySelectorAll('.sideElem'));

    }

    sidePanelShownFlag = !sidePanelShownFlag
}