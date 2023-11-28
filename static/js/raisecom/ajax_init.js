var get_port_url = "/raisecom/get_port/";
var disable_port_url = "/raisecom/disable_port/";

var get_mac_url = "/raisecom/get_errors/";

var get_errors_url = "/raisecom/get_mac/";


document.addEventListener("DOMContentLoaded", function() {
    // код, который отработает при входе на страницу

    still_active();  // подтверждает активность

    setTimeout(function() {get_port();}, 0);
    setTimeout(function() {get_errors();}, 30);

    setTimeout(function() {get_mac();}, 20);
    setTimeout(function() {get_open_port();}, 0);

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
            setTimeout(function() {get_port();}, 500);
}});}


    function get_mac() {
//    console.log('стартую запрос get_mac')
    wait_div('macInfo', 'Мак..')
    ajax_div(get_mac_url, 'macInfo', get_mac_business);}




/////////////  ФУНКЦИИ ПРАВОГО РЯДА:

function get_errors() {
    wait_div('errorsInfo', 'Порт..')
    ajax_div(get_errors_url, 'errorsInfo', get_errors_business);}
