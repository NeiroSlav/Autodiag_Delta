function get_bind_business(response) {

    var b1 = setB()
    b1['text'] = 'Состояние привязки:'
    b1['style'] = 'width: 236px;'
    b1['id'] = 'mainButton'
    b1['onclick'] = 'get_bind();'

    var bn = setB()
    bn['style'] = 'width: 236px; height: 60px;'
    bn['onclick'] = "copyDiag('bind')"

    if (response.error) {
        b1['color'] = bn['color'] = 'Red'
        b1['text'] = bn['text'] = 'ошибка диагностики'

        return getB(b1) + getB(bn);

    } else {

        bn['onclick'] = "copyDiag('bind')"

        var diagData = '! Привязок нет\n'
        if (response.ok) {
            diagData = '+ Привязка есть:\n'
        }
        for (var key in response.binding) {

            diagData += gap + key;
            if (response.binding[key][1]) {
                diagData += ' Active ' + response.binding[key][0] + '\n';
            } else {
                diagData += ' Inactive ' + response.binding[key][0] + '\n';
            }
        }
        updateDiagDict('bind', diagData)


        b1['color'] = 'Red'
        if (response.ok) {
            b1['color'] = 'Green'}

        var all_binds = ''
        for (var key in response.binding) {
            if (response.binding.hasOwnProperty(key)) {
                var list = response.binding[key];
                var bind_state = ' Inactive'
                if (list[1]) {
                    bind_state = ' Active'
                    bn['color'] = 'Green'
                }
                bind_text = list[0] + bind_state + '\n' + key
                bn['text'] = bind_text
                all_binds = all_binds + getB(bn)
            }
        }
        if (all_binds == '') {
            bn['text'] = 'привязок не обнаружено'
            all_binds = getB(bn)
        }

        return getB(b1) + all_binds;
    }
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


var util_info


function get_util_business(response) {

    console.log(response)

    var b1 = setB()
    b1['text'] = 'Трафик на порту:'
    b1['onclick'] = 'get_util();'
    b1['style'] = 'width: 236px;'
    b1['id'] = 'mainButton'
    b1['color'] = 'Green'

    var b2 = setB()
    b2['style'] = 'width: 116px;'
    b2['id'] = ''

    var b3 = setB()
    b3['style'] = 'width: 116px; margin-left: 3px;'
    b3['id'] = ''

    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = 'Red'
        b1['text'] = 'Ошибка проверки'
        b2['text'] = b3['text'] = 'Ошибка'
        return getB(b1) + getB(b2) + getB(b3)
    } else {

        b2['text'] = 'in ' + response.tx
        b3['text'] = 'out ' + response.rx

        return getB(b1) + getB(b2) + getB(b3);

    }
}
