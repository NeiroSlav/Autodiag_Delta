
function get_port_business(response) {

    var b1 = setB() // кнопка "порт:"
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB() // кнопка "100M/F"
    var b6 = setB() // кнопка "Ошибки"


    b2['style'] = 'width: 176px; margin-left: 3px;'
    b6['style'] = 'width: 176px; margin-left: 60px;'
    b2['onclick'] = b6['onclick'] = "copyDiag('port')"


    if (response.error) {
        b1['color'] = b2['color'] = 'Red'
        b2['text'] = 'ошибка'
    } else {


        var diagData = '! Порт с проблемой:\n'
        if (response.ok) {
            diagData = '+ Порт в порядке:\n'
        }

        diagData += gap + response.port + '\n' + gap + 'ошибки: ' + response.errors + '\n';
        updateDiagDict('port', diagData)


        b2['text'] = response.port
        b6['text'] = 'Ошибки: ' + response.errors

        if (response.ok) {
            b1['color'] = 'Green'
        } else {
            b1['color'] = 'Red'
        }
    }

    return getB(b1) + getB(b2) + getB(b6);
}


function get_mac_business(response) {

    var b1 = setB()
    b1['text'] = 'Мак:'
    b1['onclick'] = 'get_mac();'
    b1['id'] = 'mainButton'

    var bn = setB()
    bn['style'] = 'width: 176px; margin-left: 3px;'

    if (response.error) {
        b1['color'] = bn['color'] = 'Red'
        bn['text'] = 'ошибка'
        return getB(b1) + getB(bn);

    } else {


        var diagData = '! Маки не изучены\n'
        if (response.ok) {
            diagData = '+ Мак изучился:\n'
        }

        for (var key in response.mac) {
            diagData += gap + key;

            if (response.mac[key]) {
                diagData += ' прописан\n';
            } else {
                diagData += ' не прописан\n';
            }
        }
        updateDiagDict('mac', diagData)


        b1['color'] = 'Red'
        if (response.ok) {
            b1['color'] = 'Green'}

        var all_macs = ''
        for (var key in response.mac) {
            if (response.mac[key]) {
                bn['color'] = 'Green'
            }
            if (all_macs != '') {
                bn['style'] = 'width: 176px; margin-left: 60px;'
            }
            bn['text'] = key
            bn['onclick'] = "saveClip('"+key+"');"
            all_macs = all_macs + getB(bn)
        }
        if (all_macs == '') {
            bn['text'] = 'не изучился'
            all_macs = getB(bn)
        }

        return getB(b1) + all_macs;
    }
}
