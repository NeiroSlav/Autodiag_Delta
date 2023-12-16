
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
function wait_div(id, text, buttonId="#mainButton") {
    var block = document.getElementById(id);
    if (block) {
        var button = block.querySelector(buttonId);
        if (button) {
            button.innerText = text;
            button.style.border = "3px solid #384d84";
            button.style.background = "#384d84";
            button.style.color = "#FFF";

}}}


function replace_div(responce, divId, func) {
    var oldDiv = document.getElementById(divId);  // Достаём старый div
    oldDiv.innerHTML = func(responce);  // Дёргаем переданную функцию
}


// принимает на вход юрл, название блока, и функцию, выполняет запрос
function ajax_div(url, divId, func) {
    $.ajax({
        type: 'GET',
        url : url + token,
        dataType: 'json',
        data: {
        },
        success: function(response){
            replace_div(response, divId, func);
        },
        error: function(error){
            replace_div(error, divId, func);
        }
});}
