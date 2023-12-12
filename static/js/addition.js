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
    var oldDiv = document.getElementById('additionPanel');  // Достаём старый div

    if (additionShownFlag) { //  если панель показана, то скрыть
        oldDiv.style.width = 0 + "px";
    } else {                 //  если панель скрыта, то показать
        oldDiv.style.width = 300 + "px";
    }

    additionShownFlag = !additionShownFlag
}