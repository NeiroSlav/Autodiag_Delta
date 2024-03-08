var get_base_url = "/air/get_base/";
var get_station_url = "/air/get_station/";


document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    updateAll();

    // подтверждает активность токена раз в минуту
    setInterval(still_active, 60000);

});

function updateAll() {
    setTimeout(function() {get_base();}, 0);
    setTimeout(function() {get_station();}, 20);

}


////////////  ФУНКЦИИ ЛЕВОГО РЯДА:

function get_base() {
//    console.log('стартую запрос get_port')
    wait_div('baseInfo', 'База..')
    ajax_div(get_base_url, 'baseInfo', get_base_business);}



///////////  ФУНКЦИИ ПРАВОГО РЯДА:

function get_station() {
//    console.log('стартую запрос get_signal')
    wait_div('stationInfo', 'Станция..')
    ajax_div(get_station_url, 'stationInfo', get_station_business);}

