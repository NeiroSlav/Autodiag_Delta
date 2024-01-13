document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу
    console.log(group_tickets)


    if (group_tickets == '{}') {
        console.log(group_tickets)
        ticket_menu_init()
    }
});


var light_status = 'свет пропадал'
var link_status = 'линк есть'
var mini_block = ['<div class="diagMiniBlock">', '</div>']

function ticket_menu_init() {
//    console.log('показываю одиночную выборку');
    var div = document.getElementById('ticketField');
    div.style.height = 'auto';
    var title_button = setB;
    title_button['color'] = 'Red'
    title_button['text'] = 'Собрать тикет на ЦУС:'
    title_button['style'] = 'width: 334px;'
    div.innerHTML = getB(title_button) + get_light_block() + get_link_block() + get_submit_block();
}

function get_light_block() {

    var light1 = setB()
    var _yes = setB()
    var _no = setB()
    light1['style'] = 'width: 206px;'
    _yes['style'] = _no['style'] = 'width: 60px;'
    light1['text'] = 'свет пропадал?'
    _yes['text'] = 'да'
    _no['text'] = 'нет'
    _yes['onclick'] = "light_status = 'свет пропадал'; ticket_menu_init();"
    _no['onclick'] = "light_status = 'свет не пропадал'; ticket_menu_init();"

    if (light_status == 'свет пропадал') {
        _yes['color'] = 'Green'
    } else if (light_status == 'свет не пропадал') {
        _no['color'] = 'Green'
    }
    return getB(light1) + getB(_yes) + getB(_no)
}


function get_link_block() {

    var link1 = setB()
    var _yes = setB()
    var _no = setB()
    link1['style'] = 'width: 206px;'
    _yes['style'] = _no['style'] = 'width: 60px;'
    link1['text'] = 'линк есть?'
    _yes['text'] = 'да'
    _no['text'] = 'нет'
    _yes['onclick'] = "link_status = 'линк есть'; ticket_menu_init();"
    _no['onclick'] = "link_status = 'линка нет'; ticket_menu_init();"

    if (link_status == 'линк есть') {
        _yes['color'] = 'Green'
    } else if (link_status == 'линка нет') {
        _no['color'] = 'Green'
    }
    return getB(link1) + getB(_yes) + getB(_no)
}

function get_submit_block() {

    comment = 'Свитч лежит, ' + light_status + ', ' + link_status
    console.log(comment)

    submitB = setB()
    submitB['style'] = 'width: 334px;'
    submitB['text'] = 'Создать тикет'
    submitB['color'] = 'Blue'
    submitB['onclick'] = "createGroupTicket('', '" + comment + "');"

    return getB(submitB)
}


// очищает поле создания тикета, пишет о результате
function close_ticket_menu(response) {
    var div = document.getElementById('ticketField');
    div.style.height = '';
    messageB = setB()

    if (response.ok) {
        messageB['text'] = 'Тикет создан!'
        messageB['color'] = 'Green'
    } else {
        messageB['text'] = 'Тикет не был создан!'
        messageB['color'] = 'Red'
    }

    messageB['style'] = 'width: 300px; height: 51px; font-size: 18px; margin: 40px 0 0 17px;'
    div.innerHTML = getB(messageB);
}