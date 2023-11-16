var jsData = document.querySelector(".js-data")
function get_var(name) {
    return jsData.getAttribute(name);
}

var token = get_var("token");
var still_active_url = get_var("still_active_url");
//var watch_activity_url = get_var("watch_activity_url");

var get_port_url = get_var("get_port_url");
var get_mac_url = get_var("get_mac_url");

var get_signal_url = get_var("get_signal_url");
var get_active_url = get_var("get_active_url");

var get_open_port_url = get_var("get_open_port_url");


console.log(token);

document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    still_active();  // подтверждает активность

    setTimeout(function() {get_port();}, 0);
    setTimeout(function() {get_mac();}, 20);

    setTimeout(function() {get_signal();}, 20);
    setTimeout(function() {get_active();}, 30);

    setTimeout(function() {get_open_port();}, 0);

    // подтверждает активность токена раз в минуту
    setInterval(still_active, 60000);

});



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

