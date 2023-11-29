
function get_port_business(response) {

    var b1 = setB() // кнопка "порт:"
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB() // кнопка "100M/F"
    var b3 = setB() // кнопка "Enabled"
    var b4 = setB() // кнопка "Выкл"
    var b5 = setB() // кнопка "Аптайм"
    b2['onclick'] = b3['onclick'] = b5['onclick'] = "copyDiag('port')"


    b2['style'] = 'width: 176px;'
    b3['style'] = 'width: 116px; margin-left: 62px;'
    b5['style'] = 'width: 176px; margin-left: 62px;'


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
