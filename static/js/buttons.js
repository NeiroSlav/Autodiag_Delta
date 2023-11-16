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


function saveClip (text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'Скопировано в буфер обмена' : 'Не удалось скопировать';
        console.log(msg);
    } catch (err) {
        console.error('Ошибка при копированиХотел с консоли затеститьи: ', err);
    }
    document.body.removeChild(textArea);
}


function openInNewTab(url) {
    var newTab = window.open(url, '_blank');
    newTab.focus();
}