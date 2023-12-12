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

    if (!additionShownFlag) {
        oldDiv.style.width = 0 + "px";
    } else {
        oldDiv.style.width = 300 + "px";
    }

    additionShownFlag = !additionShownFlag
}