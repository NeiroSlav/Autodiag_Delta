

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

    b2['style'] = 'width: 116px; margin-left: 3px'
    b3['style'] = b4['style'] = b5['style'] = 'width: 116px; margin-left: 120px'

    if (response.error) {
        b1['color'] = b2['color'] = b3['color'] = b4['color'] = b5['color'] = 'Red'
        b2['text'] = b3['text'] = b4['text'] = b5['text'] = 'Ошибка'
    } else {

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
    }
    return getB(b1) + getB(b2) + getB(b3) + getB(b4) + getB(b5);
}

