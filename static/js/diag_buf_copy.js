// Инициализация словаря
let diagDict = {};

var gap = '  '

// Функция добавления или обновления ключа в словаре
function updateDiagDict(key, data) {
    diagDict[key] = data;
    console.log('diagDict updated!')
}


function saveClip (text) {
    // Создаем временный элемент textarea для копирования в буфер обмена
    var tempTextarea = document.createElement("textarea");
    tempTextarea.value = text;

    // Добавляем элемент в DOM и выделяем его содержимое
    document.body.appendChild(tempTextarea);
    tempTextarea.select();

    // Копируем выделенное в буфер обмена
    document.execCommand('copy');

    // Удаляем временный элемент
    document.body.removeChild(tempTextarea);

}


// Функция копирования данных из словаря в буфер обмена по ключу
function copyDiag(key) {
    let copyString = '';

    // Проверяем, существует ли ключ в словаре
    if (key in diagDict) {

        // строка для копирования
        copyString += diagDict[key] + '\n';
        let rows = copyString.split('\n');
        rows = rows.slice(1);
        copyString = rows.join('\n');

    } else {

         // Перебираем все ключи и значения в словаре
        for (const key in diagDict) {
            if (diagDict.hasOwnProperty(key)) {
                copyString += diagDict[key] + '\n';
            }
        }
    }
    saveClip(copyString);
}
