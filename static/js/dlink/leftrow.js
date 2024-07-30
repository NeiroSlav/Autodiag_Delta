// код после внедрения функций

function get_port_business(response) {

    var b1 = setB()
    b1['text'] = 'Порт:'
    b1['onclick'] = 'get_port();'
    b1['id'] = 'mainButton'

    var b2 = setB()
    var bDescLeft = setB()
    var bDesc = setB()
    var b3 = setB()

    b2['style'] = 'width: 176px;'
    bDesc['style'] = 'width: 176px;'
    b3['style'] = 'width: 116px; margin-left: 62px;'
    b2['onclick'] = b3['onclick'] = bDescLeft['onclick'] = bDesc['onclick'] = "copyDiag('port')"

    var b4 = setB()
    b4['color'] = 'Blue'

    if (response.error) {
        b1['color'] = b2['color'] = bDesc['color'] = b3['color'] = 'Red'
        b2['text'] = bDesc['text'] = b3['text'] = 'ошибка'
        b4['text'] = '-'
    } else {

        var diagData = '! Состояние порта:\n'
        if (response.ok) {
            diagData = '+ Состояние порта:\n'
        }

        diagData += gap + response.enabled + '\n' + gap + response.port + '\n';

        if (response.desc) {
            diagData += gap + 'Описание: ' + response.desc + '\n';
        }

        updateDiagDict('port', diagData)


        b2['text'] = response.port

        bDescLeft['text'] = 'Опис:'
        if (response.desc) {
            bDesc['text'] = response.desc;
        }

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

    descData = ''
    if (response.desc) {
        descData += getB(bDescLeft) + getB(bDesc)
    }

    return getB(b1) + getB(b2) + descData + getB(b3) + getB(b4);
}


function get_errors_business(response) {

    var b1 = setB()
    b1['text'] = 'Ошибки:'
    b1['onclick'] = 'get_errors();'
    b1['id'] = 'mainButton'

    var b2 = setB()
    var b3 = setB()
    var b4 = setB()

    var b5 = setB()
    var b6 = setB()
    var b7 = setB()

    var b9 = setB()
    b9['color'] = 'Blue'
    b9['onclick'] = 'clear_counter();'

    b2['onclick'] = b3['onclick'] = b4['onclick'] = "copyDiag('errors')"
    b5['onclick'] = b6['onclick'] = b7['onclick'] = "copyDiag('errors')"

    b1['style'] = b2['style'] = b3['style'] = b4['style'] = 'width: 116px;'
    b9['style'] = b5['style'] = b6['style'] = b7['style'] = 'width: 116px;'


    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = b4['color'] = 'Red'
        b5['color'] = b6['color'] = b7['color'] = 'Red'

        b2['text'] = b3['text'] = b4['text'] = 'Ошибка'
        b5['text'] = b6['text'] = b7['text'] = 'Ошибка'

        b9['text'] = '-'

        return getB(b1) + getB(b9) + getB(b2) + getB(b5) + getB(b3) + getB(b6) + getB(b4) + getB(b7);
    } else {

        var diagData = '! Есть ошибки:\n'
        if (response.ok) {
            diagData = '+ Ошибок нет :\n'
        }

        diagData += gap + 'crc error : ' + response.rx.crc + '\n';
        diagData += gap + 'fragment : ' + response.rx.frg + '\n';
        diagData += gap + 'jabber : ' + response.rx.jab + '\n';


        if (!response.ok_tx) {
            diagData += '\n';
            diagData += gap + 'deferral : ' + response.tx.xdef + '\n';
            diagData += gap + 'late coll : ' + response.tx.lcol + '\n';
            diagData += gap + 'excess coll : ' + response.tx.xcol + '\n';
            diagData += gap + 'single coll : ' + response.tx.scol + '\n';
            diagData += gap + 'collision : ' + response.tx.col + '\n';
        }

        updateDiagDict('errors', diagData)


        if (response.ok) {
            b1['color'] = 'Green'
        } else {
            if (response.rx.crc != '0') {
                b2['color'] = 'Red'}
            if (response.rx.frg != '0') {
                b3['color'] = 'Red'}
            if (response.rx.jab != '0') {
                b4['color'] = 'Red'}
            b1['color'] = 'Red'
        }

        b2['text'] = 'crc ' + response.rx.crc
        b3['text'] = 'frg ' + response.rx.frg
        b4['text'] = 'jab ' + response.rx.jab
        b9['text'] = 'Очистить'

        var count = 3
        var i = 0
        var tx_row = [b5, b6, b7]
        var already = []

        while (i<count) {
            var biggest = -1
            var add = ''
            console.log(i)

            for (const [key, value] of Object.entries(response.tx)) {
                if ( parseInt(value) > biggest && !(already.includes(key)) ) {
                    biggest = parseInt(value)
                    console.log(key, value)
                    tx_row[i]['text'] = key + ' ' + value
                    if (value != '0') {
                        tx_row[i]['color'] = 'Red'
                    }
                    add = key
                }
            }
            already.push(add)
        console.log(already)
        i++
        }
    }
    return getB(b1) + getB(b9) + getB(b2) + getB(tx_row[2]) + getB(b3) + getB(tx_row[1]) + getB(b4) + getB(tx_row[0]);
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

        var diagData = '! Состояние кабеля:\n'
        if (response.ok) {
            diagData = '+ Состояние кабеля:\n'
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