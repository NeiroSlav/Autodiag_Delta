var getAdditionHtml = '' +
                '<div class="diagLongBlock">' +
                    '<div style="margin-bottom: 40px;"></div>' +
                    '<div class="diagMiniBlock">' +
                        '<div class="diagLog"></div>' +
                        '<button class="diagButtonRed">obabok</button>' +
                    '</div>' +
            '</div>'


var additionShownFlag = false

function showAddition() {
    // console.log(responce);
    var additionPanel = document.getElementById('additionPanel');  // Достаём div
    var sepRight = document.getElementById('sepRight');
    var mainPanel = document.getElementById('mainPanel');


    if (additionShownFlag) { //  если панель показана, то скрыть
        additionPanel.style.width = 0;
        sepRight.style.width = 0;
        mainPanel.style.padding = "0 48px 0 48px";

    } else {                 //  если панель скрыта, то показать
        additionPanel.style.width = 272 + "px";
        sepRight.style.width = 24 + "px";
        mainPanel.style.padding = "0 12px 0 12px";

    }

    additionShownFlag = !additionShownFlag
}