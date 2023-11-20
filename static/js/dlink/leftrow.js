// код после внедрения функций

function get_port_business(response) {

    var b1 = setB()
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB()
    var b3 = setB()
    var b4 = setB()

    b2['style'] = 'width: 176px; margin-left: 3px;'
    b3['style'] = 'width: 116px; margin-left: 60px;'
    b4['style'] = 'margin-left: 3px;'
    b2['onclick'] = b3['onclick'] = "copyDiag('port')"

    b4['color'] = 'Blue'
    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = 'Red'
        b2['text']= b3['text'] = 'ошибка'
        b4['text'] = '-'
    } else {

        var diagData = '! Порт с проблемой:\n'
        if (response.ok) {
            diagData = '+ Порт в порядке:\n'
        }

        diagData += gap + response.enabled + '\n' + gap + response.port + '\n';
        updateDiagDict('port', diagData)


        b2['text'] = response.port
        b3['text'] = response.enabled

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

    return getB(b1) + getB(b2) + getB(b3) + getB(b4);
}


function get_errors_business(response) {

    var b1 = setB()
    b1['text'] = 'Ошибки:'
    b1['style'] = 'width: 116px;'
    b1['onclick'] = 'get_errors();'
    b1['id'] = 'mainButton'


    var b2 = setB()
    var b3 = setB()
    var b4 = setB()
    var b5 = setB()
    var b6 = setB()
    b2['onclick'] = b3['onclick'] = b4['onclick'] = b5['onclick'] = "copyDiag('errors')"


    b2['style'] = 'width: 116px; margin-left: 3px'
    b3['style'] = b4['style'] = b5['style'] = b6['style'] = 'width: 116px; margin-left: 120px'
    b6['color'] = 'Blue'
    b6['onclick'] = 'clear_counter();'

    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = b4['color'] = b5['color'] = 'Red'
        b2['text'] = b3['text'] = b4['text'] = b5['text'] = 'Ошибка'
        b6['text'] = '-'
    } else {


        var diagData = '! Есть ошибки:\n'
        if (response.ok) {
            diagData = '+ Ошибок нет :\n'
        }

        diagData += gap + 'crc      : ' + response.errors.crc + '\n';
        diagData += gap + 'fragment : ' + response.errors.fragment + '\n';
        diagData += gap + 'jabber   : ' + response.errors.jabber + '\n';
        diagData += gap + 'drop     : ' + response.errors.drop + '\n';

        updateDiagDict('errors', diagData)


        if (response.ok) {
            b1['color'] = 'Green'
        } else {
            if (response.errors.crc != '0') {
                b2['color'] = 'Red'}

            if (response.errors.fragment != '0') {
                b3['color'] = 'Red'}

            if (response.errors.jabber != '0') {
                b4['color'] = 'Red'}

            if (response.errors.drop != '0') {
                b5['color'] = 'Red'}

            b1['color'] = 'Red'
        }
        b2['text'] = 'crc ' + response.errors.crc
        b3['text'] = 'frag ' + response.errors.fragment
        b4['text'] = 'jab ' + response.errors.jabber
        b5['text'] = 'drop ' + response.errors.drop
        b6['text'] = 'очистить'
    }
    return getB(b1) + getB(b2) + getB(b3) + getB(b4) + getB(b5) + getB(b6);
}

function get_cable_business(response) {

    var b1 = setB()
    b1['text'] = 'Диагностика кабеля:'
    b1['style'] = 'width: 236px;'
    b1['onclick'] = 'get_cable();'
    b1['id'] = 'mainButton'

    var bn = setB()
    bn['style'] = 'width: 236px'
    bn['onclick'] = "copyDiag('cable')"


    if (response.error) {
        b1['color'] = bn['color'] = 'Red'
        bn['text'] = 'ошибка диагностики'
        return getB(b1) + getB(bn);

    } else {

        var diagData = '! Проблемный кт:\n'
        if (response.ok) {
            diagData = '+ Кабель в порядке:\n'
        }

        for (var n in response.cable) {
            diagData += gap + response.cable[n] + '\n';
        }
        updateDiagDict('cable', diagData)


        b1['color'] = 'Red'
        if (response.ok) {
            b1['color'] = 'Green'}

        var all_pares = ''
        for (var n in response.cable) {
            bn['text'] = response.cable[n]
            all_pares = all_pares + getB(bn)
        }
        return getB(b1) + all_pares;
    }
}