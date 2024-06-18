
// отправляет запрос на сервер
function still_active() {
    $.ajax({
        type: 'GET',
        url : still_active_url + token,
        dataType: 'json',
        data: {
        },
});}


function changeTheme() {
    $.ajax({
        type: 'GET',
        url : change_theme_url + token,
        dataType: 'json',
        data: {
        },
});
    location.reload();
}


// принимает на вход название блока и текст, меняет текст кнопки mainButton в блоке
function wait_div(id, text, buttonId="#mainButton") {
    var block = document.getElementById(id);
    if (block) {
        var button = block.querySelector(buttonId);
        if (button) {
            button.innerText = text;
            button.style.border = "3px solid var(--act-color)";
            button.style.background = "var(--act-color)";
            button.style.color = "#FFF";

}}}


function replace_div(response, divId, func) {
    var oldDiv = document.getElementById(divId);  // Достаём старый div
    oldDiv.innerHTML = func(response);  // Дёргаем переданную функцию
}


// принимает на вход юрл, название блока, и функцию, выполняет запрос
function ajax_div(url, divId, func, final) {
    $.ajax({
        type: 'GET',
        url : url + token,
        dataType: 'json',
        data: {
        },
        success: function(response){
            replace_div(response, divId, func);
            if (final != undefined) {final()};
        },
        error: function(error){
            replace_div(error, divId, func);
            if (final != undefined) {final()};
        }
});}


function createTicket(ticket_id, comment) {
    console.log(ticket_id)
    console.log(user)
    console.log(anumber)

    var input_field = document.getElementById('phoneInput');
    var phone = input_field.value
    if (phone == '') {
        phone = 'телефон не указан'
    }

    $.ajax({
        type: 'GET',
        url : '/create_ticket',
        dataType: 'json',
        data: {
            user: user,
            anumber: anumber,
            ticket_id: ticket_id,
            comment: abon_login+ ', ' + phone + ', ' + comment ,
        },
        success: function(response){
            close_ticket_menu(response);
//            replace_div(response, divId, func);
        },
        error: function(error){
            close_ticket_menu({'ok': false});
//            replace_div(error, divId, func);
        }
});
}