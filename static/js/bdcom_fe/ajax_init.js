var get_port_url = "/bdcom_fe/get_port/";
var get_mac_url = "/bdcom_fe/get_mac/";


document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    updateAll();
    setTimeout(function() {get_open_port();}, 0);

    // подтверждает активность токена раз в минуту
    setInterval(still_active, 60000);

});

function updateAll() {
    setTimeout(function() {get_port();}, 0);
    setTimeout(function() {get_mac();}, 20);
}


////////////  ФУНКЦИИ ЛЕВОГО РЯДА:

function get_port() {
//    console.log('стартую запрос get_port')
    wait_div('portInfo', 'Порт..')
    ajax_div(get_port_url, 'portInfo', get_port_business);}

function get_mac() {
//    console.log('стартую запрос get_mac')
    wait_div('macInfo', 'Мак..')
    ajax_div(get_mac_url, 'macInfo', get_mac_business);}
