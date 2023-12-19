document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    if (group_ticket == 'None') {
        ticket_menu_init()
    }
});


var light_status = ''
var link_status = ''
var mini_block = ['<div class="diagMiniBlock">', '</div>']

function ticket_menu_init() {
    console.log('показываю одиночную выборку');
    var div = document.getElementById('ticketField');
    div.style.height = 'auto';
    div.innerHTML = get_light_block() + get_link_block() + get_submit_block();
}

function get_light_block() {
    var long_block = ['<div class="diagLongBlock" style="margin: 0 auto 0 auto;">', '</div>']

    var light1 = setB()
    var light2 = setB()
    var light3 = setB()
    light1['style'] = light2['style'] = light3['style'] = 'width: 240px;'
    light1['text'] = 'свет пропадал'
    light2['text'] = 'свет не пропадал'
    light3['text'] = 'нет информации'
    light1['onclick'] = "light_status = 'свет пропадал'; ticket_menu_init();"
    light2['onclick'] = "light_status = 'свет не пропадал'; ticket_menu_init();"
    light3['onclick'] = "light_status = ''; ticket_menu_init();"

    if (light_status == 'свет пропадал') {
        light1['color'] = 'Green'
    } else if (light_status == 'свет не пропадал') {
        light2['color'] = 'Green'
    } else if (light_status == '') {
        light3['color'] = 'Green'
    }
    return long_block[0] +
           mini_block[0] + mini_block[1] +
           mini_block[0] + getB(light1) + getB(light2) + getB(light3) + mini_block[1] +
           mini_block[0] + mini_block[1] +
           long_block[1]
}


function get_link_block() {
    var long_block = ['<div class="diagLongBlock" style="margin: 0 auto 0 0;">', '</div>']

    var link1 = setB()
    var link2 = setB()
    var link3 = setB()
    link1['style'] = link2['style'] = link3['style'] = 'width: 240px;'
    link1['text'] = 'линка нет (скнп)'
    link2['text'] = 'линк есть (поио)'
    link3['text'] = 'нет информации'
    link1['onclick'] = "link_status = 'линка нет (скнп)'; ticket_menu_init();"
    link2['onclick'] = "link_status = 'линк есть (поио)'; ticket_menu_init();"
    link3['onclick'] = "link_status = ''; ticket_menu_init();"

    if (link_status == 'линка нет (скнп)') {
        link1['color'] = 'Green'
    } else if (link_status == 'линк есть (поио)') {
        link2['color'] = 'Green'
    } else if (link_status == '') {
        link3['color'] = 'Green'
    }
    return long_block[0] +
           mini_block[0] + mini_block[1] +
           mini_block[0] + getB(link1) + getB(link2) + getB(link3) + mini_block[1] +
           mini_block[0] + mini_block[1] +
           long_block[1]
}

function get_submit_block() {
    var long_block = ['<div class="diagLongBlock" style="margin: 0 auto 0 0;">', '</div>']

    preView = setB()
    preView['style'] = 'width: 240px; height: 60px;'
    comment = 'Свитч лежит'
    if (light_status) {
        comment += ',<br>' + light_status
    }

    if (link_status) {
        comment += ',<br>' + link_status
    }

    preView['text'] = comment
    comment = comment.replace('<br>', ' ').replace('<br>', ' ')
    console.log(comment)

    submitB = setB()
    submitB['style'] = 'width: 240px;'
    submitB['text'] = 'Создать тикет!'
    submitB['color'] = 'Blue'
    submitB['onclick'] = "createGroupTicket('" + user + "','" + anumber + "','" + group_ticket + "','" + comment + "');"

    return long_block[0] +
           mini_block[0] + mini_block[1] +
           mini_block[0] + getB(preView) + getB(submitB) + mini_block[1] +
           mini_block[0] + mini_block[1] +
           long_block[1]
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

    messageB['style'] = 'width: 400px; height: 40px; font-size: 18px; margin: auto auto auto auto;'
    div.innerHTML = getB(messageB);
}