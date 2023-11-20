function setB () {
    return {'color': '', 'id': '', 'style': '', 'onclick': '', 'text': ''};
}

function getB (button) {
    text = '<button '+
           'class="diagButton'+button['color']+
           '" id="'+button['id']+
           '" style="'+button['style']+
           '" onclick="'+button['onclick']+
           '">'+button['text']+'</button>';

    return text.replace('undefined', '')
}


function openInNewTab(url) {
    var newTab = window.open(url, '_blank');
    newTab.focus();
}