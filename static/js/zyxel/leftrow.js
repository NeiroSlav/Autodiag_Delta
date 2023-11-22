
function get_port_business(response) {

    var b1 = setB() // кнопка "порт:"
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB() // кнопка "100M/F"
    var b3 = setB() // кнопка "Enabled"
    var b4 = setB() // кнопка "Выкл"
    var b5 = setB() // кнопка "Аптайм"
    var b6 = setB() // кнопка "Ошибки"


    b2['style'] = 'width: 176px; margin-left: 3px;'
    b3['style'] = 'width: 116px; margin-left: 60px;'
    b4['style'] = 'margin-left: 3px;'
    b5['style'] = 'width: 176px; margin-left: 60px;'
    b6['style'] = 'width: 176px; margin-left: 60px;'
    b2['onclick'] = b3['onclick'] = b5['onclick'] = b6['onclick'] = "copyDiag('port')"

    b4['color'] = 'Blue'
    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = b5['color'] = b6['color'] = 'Red'
        b2['text']= b3['text'] = b5['text']= b6['text'] = 'ошибка'
        b4['text'] = '-'
    } else {


        var diagData = '! Порт с проблемой:\n'
        if (response.ok) {
            diagData = '+ Порт в порядке:\n'
        }

        diagData += gap + response.enabled + '\n' + gap + response.port + '\n';
        diagData += gap + response.uptime + '\n' + gap + '' + response.errors + '\n';
        updateDiagDict('port', diagData)


        b2['text'] = response.port
        b3['text'] = response.enabled
        b5['text'] = 'АпТайм: ' + response.uptime
        b6['text'] = 'Ошибки: ' + response.errors

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


    return getB(b1) + getB(b2) + getB(b5) + getB(b6) + getB(b3) + getB(b4);
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