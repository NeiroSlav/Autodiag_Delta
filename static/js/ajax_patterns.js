
// отправляет запрос на сервер
function still_active() {
    $.ajax({
        type: 'GET',
        url : still_active_url + token,
        dataType: 'json',
        data: {
        },
});}


// принимает на вход название блока и текст, меняет текст кнопки mainButton в блоке
function wait_div(id, text) {
    var block = document.getElementById(id);
    if (block) {
        var button = block.querySelector("#mainButton");
        if (button) {
            button.innerText = text;
            button.style.border = "2px solid #999999";
}}}


// принимает на вход юрл, название блока, и функцию, выполняет запрос
function ajax_div(url, divId, func) {
    $.ajax({
        type: 'GET',
        url : url + token,
        dataType: 'json',
        data: {
        },
        success: function(response){
            console.log(response);
            var oldDiv = document.getElementById(divId);  // Достаём старый div
            var newDiv = document.createElement("div");  // Создаём новый div
            newDiv.setAttribute("id", divId);
            newDiv.setAttribute("class", "diagMiniBlock");
            console.log(newDiv)
            newDiv.innerHTML = func(response);  // Дёргаем переданную функцию
            oldDiv.parentNode.replaceChild(newDiv, oldDiv);  // Заменяем старый div новым
        },
        error: function(error){
            console.log(error);
            var oldDiv = document.getElementById(divId);  // Достаём старый div
            var newDiv = document.createElement("div");  // Создаём новый div
            newDiv.setAttribute("id", divId);
            newDiv.setAttribute("class", "diagMiniBlock");
            console.log(newDiv)
            newDiv.innerHTML = func({'error': true});  // Дёргаем переданную функцию
            oldDiv.parentNode.replaceChild(newDiv, oldDiv);  // Заменяем старый div новым
        }
});}
