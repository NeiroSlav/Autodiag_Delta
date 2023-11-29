
function get_open_port() {
//    console.log('стартую запрос get_open_port')
    wait_div('openPortInfo', 'Открытый порт..')
    ajax_div(get_open_port_url, 'openPortInfo', get_open_port_business);}


function get_open_port_business(response) {

    var b1 = setB()
    b1['text'] = 'Открытых портов'
    b1['onclick'] = 'get_open_port();'
    b1['style'] = 'width: 176px;'
    b1['id'] = 'mainButton'

    var b2 = setB()

    if (response.port) {
        b1['color'] = b2['color'] = 'Green'
        b1['text'] = 'Открытый порт:'
        b2['text'] = response.port
        b2['onclick'] = "openInNewTab('http://" + response.ip + ":" + response.port + "');"
        return getB(b1) + getB(b2);

    } else {
        b1['color'] = ''
        b2['text'] = 'нет'
        return getB(b1) + getB(b2);
    }
}
