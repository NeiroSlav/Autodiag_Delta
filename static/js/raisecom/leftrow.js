
function get_port_business(response) {

    var b1 = setB() // кнопка "порт:"
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB() // кнопка "100M/F"
    var b3 = setB() // кнопка "Enabled"
    var b5 = setB() // кнопка "Аптайм"


    b2['style'] = 'width: 176px; margin-left: 3px;'
    b3['style'] = 'width: 116px; margin-left: 60px;'
    b5['style'] = 'width: 176px; margin-left: 60px;'
    b2['onclick'] = b3['onclick'] = b5['onclick'] = "copyDiag('port')"

    b4['style'] = 'margin-left: 3px;'
    var b4 = setB() // кнопка "Выкл"
    b4['color'] = 'Blue'
    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = b4['color'] = b5['color'] = 'Red'
        b2['text']= b3['text'] = b4['text']= b5['text'] = 'ошибка'
        b4['text'] = '-'
    } else {


        var diagData = '! Порт с проблемой:\n'
        if (response.ok) {
            diagData = '+ Порт в порядке:\n'
        }

        diagData += gap + response.enabled + '\n' + gap + response.port + '\n';
        diagData += gap + response.uptime + '\n';
        updateDiagDict('port', diagData)


        b2['text'] = response.port
        console.log(response.enabled)
        b3['text'] = response.enabled
        b5['text'] = response.uptime

        if (response.ok) {
            b1['color'] = 'Green'
        } else {
            b1['color'] = 'Red'
        }

        if (response.enabled == 'Enabled') {
            b4['text'] = 'Выкл'
            b4['onclick'] = "disable_port('false');"
        } else {
            b4['text'] = 'Вкл'
            b4['onclick'] = "disable_port('true');"
        }
    }

    console.log(b1)
    console.log(getB(b1))


    return getB(b1) + getB(b2) + getB(b5) + getB(b3) + getB(b4);
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

