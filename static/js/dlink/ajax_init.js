var get_port_url = "/dlink/get_port/";
var disable_port_url = "/dlink/disable_port/";
var get_errors_url = "/dlink/get_errors/";
var clear_url = "/dlink/clear/";
var get_cable_url = "/dlink/cable_diag/";

var get_bind_url = "/dlink/get_bind/";
var get_mac_url = "/dlink/get_mac/";
var get_util_url = "/dlink/get_util/";

var get_log_url = "/dlink/get_log/";
var get_full_log_url = "/dlink/get_full_log/";


console.log(token);


document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    updateAll();
    setTimeout(function() {get_open_port();}, 0);
    setTimeout(function() {get_log();}, 100);

    // подтверждает активность токена раз в минуту
    setInterval(still_active, 60000);

});


function updateAll() {
    setTimeout(function() {get_port();}, 0);
    setTimeout(function() {get_errors();}, 15);
    setTimeout(function() {get_cable();}, 30);

    setTimeout(function() {get_bind();}, 45);
    setTimeout(function() {get_mac();}, 60);
    setTimeout(function() {get_util();}, 75);
}


////////////  ФУНКЦИИ ЛЕВОГО РЯДА:

function get_port() {
//    console.log('стартую запрос get_port')
    wait_div('portInfo', 'Порт..')
    ajax_div(get_port_url, 'portInfo', get_port_business);}


function disable_port(enable_var) {
    $.ajax({
        type: 'GET',
        url : disable_port_url + token,
        dataType: 'json',
        data: {
        enable: enable_var
        },
        success: function(response){
            console.log(response);
            setTimeout(function() {get_port();}, 500);
}});}


function get_errors() {
//    console.log('стартую запрос get_errors')
    wait_div('errorsInfo', 'Ошибки.')
    ajax_div(get_errors_url, 'errorsInfo', get_errors_business);}


function clear_counter() {
    console.log('вошёл');
    $.ajax({
        type: 'GET',
        url : clear_url + token,
        dataType: 'json',
        data: {
        },
        success: function(response){
            console.log(response);
            setTimeout(function() {get_errors();}, 500);
}});}


function get_cable() {
//    console.log('стартую запрос get_cable')
    wait_div('cableInfo', 'Проверяю кабель..')
    ajax_div(get_cable_url, 'cableInfo', get_cable_business);}



////////////  ФУНКЦИИ СРЕДНЕГО РЯДА:

function get_bind() {
//    console.log('стартую запрос get_bind')
    wait_div('bindInfo', 'Состояние привязки..')
    ajax_div(get_bind_url, 'bindInfo', get_bind_business);}


function get_mac() {
//    console.log('стартую запрос get_mac')
    wait_div('macInfo', 'Мак..')
    ajax_div(get_mac_url, 'macInfo', get_mac_business);}


function get_util() {
//    console.log('стартую запрос get_util')
    wait_div('utilInfo', 'Проверка трафика..')
    ajax_div(get_util_url, 'utilInfo', get_util_business);}


function get_open_port() {
//    console.log('стартую запрос get_open_port')
    wait_div('openPortInfo', 'Открытый порт..')
    ajax_div(get_open_port_url, 'openPortInfo', get_open_port_business);}


/////////////  ФУНКЦИИ ПРАВОГО РЯДА:

function get_log() {
//    console.log('стартую запрос get_open_port')
    wait_div('logInfo', 'Проверяю..')
    ajax_div(get_log_url, 'logInfo', get_log_business);}


function get_full_log() {
//    console.log('стартую запрос get_open_port')
    wait_div('logInfo', 'Проверяю..', buttonId='#mainButton2')
    ajax_div(get_full_log_url, 'logInfo', get_full_log_business);}

