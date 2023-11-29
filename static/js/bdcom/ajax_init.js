var get_port_url = "/bdcom/get_port/";
var get_mac_url = "/bdcom/get_mac/";

var get_signal_url = "/bdcom/get_signal/";
var get_active_url = "/bdcom/get_active/";


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

    setTimeout(function() {get_signal();}, 20);
    setTimeout(function() {get_active();}, 30);
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



/////////////  ФУНКЦИИ ПРАВОГО РЯДА:

function get_signal() {
//    console.log('стартую запрос get_signal')
    wait_div('signalInfo', 'Сигнал смотрю..')
    ajax_div(get_signal_url, 'signalInfo', get_signal_business);}


function get_active() {
//    console.log('стартую запрос get_active')
    wait_div('activeInfo', 'Смотрю список неактивных..')
    ajax_div(get_active_url, 'activeInfo', get_active_business);}

