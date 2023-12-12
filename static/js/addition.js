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
    var newDiv = document.createElement("div");  // Создаём новый div
    newDiv.setAttribute("id", 'additionPanel');
    newDiv.setAttribute("style", "margin: 0 auto 0 0;");

    if (!additionShownFlag) {
        newDiv.setAttribute("class", "mainFrameSub");
        newDiv.innerHTML = getAdditionHtml;
    }


    additionShownFlag = !additionShownFlag
    oldDiv.parentNode.replaceChild(newDiv, oldDiv);  // Заменяем старый div новым
}