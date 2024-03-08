function get_station_business (response) {

    console.log(response)

    var bInfo = setB() // кнопка "информация с базы:"
    bInfo['text'] = 'Станция:'
    bInfo['color'] = 'Green'
    bInfo['style'] = 'width: 86px;'
    bInfo['onclick'] = 'get_station();'
    bInfo['id'] = 'mainButton'

    var bIp = setB() // кнопка с ип базы
    bIp['text'] = station_ip
    bIp['style'] = 'width: 146px; margin-bottom: 32px;'
    bIp['onclick'] = "saveClip('"+station_ip+"');"


    if (response.error) {
        bInfo['color'] = bIp['color'] = 'Red'
        var bError = setB()
        bError['color'] = 'Red'
        bError['text'] = 'Ошибка запроса'
        bError['style'] = 'width: 236px; height: 220px;'
        return getB(bInfo) + getB(bIp) + getB(bError);
    } else {
        var topButtons = getB(bInfo) + getB(bIp)


        var bn_ = setB()
        var bn = setB()
        bn['style'] = bn_['style'] = 'width: 116px;'
        bn_['text'] = 'Lan speed:'
        bn['text'] = response.link.lan_speed
        var all_links = getB(bn_) + getB(bn)
        for (var key in response.link.interfaces) {
            bn_['text'] = key
            bn['text'] = 'link ' + response.link.interfaces[key].link
            if (response.link.interfaces[key].link == 'up') {
                bn['color'] = 'Green'
            } else {
                bn['color'] = 'Red'
            }
            all_links = all_links + getB(bn_) + getB(bn)
        }


        bn['style'] = 'width: 176px;'
        var all_macs = ''
        for (var key in response.mac) {
            if (response.mac[key]) {
                bn['color'] = 'Green'
            }
            if (all_macs != '') {
                bn['style'] = 'width: 176px; margin-left: 62px;'
            }
            bn['text'] = key
            bn['onclick'] = "saveClip('"+key+"');"
            all_macs = all_macs + getB(bn)
        }
        if (all_macs == '') {
            bn['text'] = 'не изучился'
            all_macs = getB(bn)
        }
        var bMac = setB()
        bMac['text'] = 'Мак:'
        bMac['style'] = 'margin-top: 36px;'
        all_macs = getB(bMac) + all_macs;

    }

    return topButtons + all_links + all_macs;
}
