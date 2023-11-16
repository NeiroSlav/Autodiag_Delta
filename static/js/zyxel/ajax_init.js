var jsData = document.querySelector(".js-data")
function get_var(name) {
    return jsData.getAttribute(name);
}

var token = get_var("token");
var still_active_url = get_var("still_active_url");
//var watch_activity_url = get_var("watch_activity_url");

var get_port_url = get_var("get_port_url");
var disable_port_url = get_var("disable_port_url");
var get_cable_url = get_var("get_cable_url");

var get_mac_url = get_var("get_mac_url");
var get_open_port_url = get_var("get_open_port_url");

var get_log_url = get_var("get_log_url");


console.log(token);

document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    still_active();  // подтверждает активность

    setTimeout(function() {get_port();}, 0);
    setTimeout(function() {get_cable();}, 20);

    setTimeout(function() {get_mac();}, 40);
    setTimeout(function() {get_open_port();}, 0);

    setTimeout(function() {get_log();}, 100);

    // подтверждает активность токена раз в минуту
    setInterval(still_active, 60000);

});



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
            setTimeout(function() {get_port();}, 2000);
}});}


function get_cable() {
//    console.log('стартую запрос get_cable')
    wait_div('cableInfo', 'Проверяю кабель..')
    ajax_div(get_cable_url, 'cableInfo', get_cable_business);}



////////////  ФУНКЦИИ СРЕДНЕГО РЯДА:


function get_mac() {
//    console.log('стартую запрос get_mac')
    wait_div('macInfo', 'Мак..')
    ajax_div(get_mac_url, 'macInfo', get_mac_business);}


function get_open_port() {
//    console.log('стартую запрос get_open_port')
    wait_div('openPortInfo', 'Открытый порт..')
    ajax_div(get_open_port_url, 'openPortInfo', get_open_port_business);}


/////////////  ФУНКЦИИ ПРАВОГО РЯДА:

function get_log() {
//    console.log('стартую запрос get_open_port')
    wait_div('logInfo', 'Проверяю записи лога...')
    ajax_div(get_log_url, 'logInfo', get_log_business);}
