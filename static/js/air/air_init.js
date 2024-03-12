function air_prompt_show() {
    var cover_div = document.getElementById('myPrompt')
    cover_div.style.display = 'block'
    setTimeout(() => {
      cover_div.style.opacity = 1;
    }, "10");
}

function air_prompt_close() {
    var cover_div = document.getElementById('myPrompt')
    cover_div.style.opacity = 0
    setTimeout(() => {
      cover_div.style.display = 'none';
    }, "500");
}

function open_air_page() {
    var base_ip = document.getElementById('baseIp').value
    var station_ip = document.getElementById('stationIp').value

    openInNewTab('http://adiag.entele.net:8000/air_init/' + token +
                 '?base_ip=' + base_ip +
                 '&station_ip=' + station_ip);
}