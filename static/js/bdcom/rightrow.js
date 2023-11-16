function get_signal_business (response) {

    var b1 = setB()
    b1['onclick'] = 'get_signal();'
    b1['style'] = 'width: 176px;'
    b1['id'] = 'mainButton'

    var b2 = setB()
    b2['style'] = 'margin-left: 3px;'


    if (response.error) {  // если вернулась ошибка
        b1['color'] = b2['color'] = 'Red'
        b1['text'] = 'Ошибка сигнала'
        b2['text'] = '-'
        return getB(b1) + getB(b2)
    } else {

        b2['text'] = response.signal

        if (response.ok) {
            b1['color'] = 'Green'
            b1['text'] = 'Сигнал хороший'
        } else {
            b1['color'] = 'Red'
            b1['text'] = 'Сигнал плохой'
        }

        return getB(b1) + getB(b2)
    }}


function get_active_business (response) {

var b1 = setB()
b1['onclick'] = 'get_active();'
b1['style'] = 'width: 236px;'
b1['id'] = 'mainButton'


if (response.error) {  // если вернулась ошибка
    b1['color'] = 'Red'
    b1['text'] = 'Ошибка проверки неактивных'
    return getB(b1)
} else {

    if (response.ok) {
        b1['color'] = 'Green'
        b1['text'] = 'Нет в списке неактивных'
    } else {
        b1['color'] = 'Red'
        b1['text'] = 'Есть в списке неактивных'
    }

    return getB(b1)
}}