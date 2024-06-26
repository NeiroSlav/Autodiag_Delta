class UserSettings:
    """
    Класс настроек пользователя.
    Вытягивает данные из файла user_settings.txt в виде словаря

    Пример синтаксиса элемента настроек в файле:
        username             param:arg param2:arg2

    Его же ключ-значение в словаре self.data:
        'username': {'param': 'arg', 'param2': 'arg2'}
    """

    def __init__(self):
        self.data = {}
        self._fetch()

    # забирает данные из файла user_settings.txt
    def _fetch(self):
        with open("init/user_settings.txt") as file:
            for line in file:
                username, *value = line.split()
                self.data[username] = {}
                for elem in value:
                    _key, _value = elem.split(':')
                    self.data[username][_key] = _value

    # возвращает дефолтные значения
    @staticmethod
    def _default() -> dict:
        return {'theme': 'dark',
                'panel': 'hidden',
                'division': 'otp'}

    # сохраняет настройки в файл user_settings.txt
    def _save(self) -> None:
        with open('init/user_settings.txt', 'w') as file:
            _to_write = ''
            for username, value in self.data.items():
                res = ''
                for k, v in value.items():
                    res += f' {k}:{v: <10}'
                _to_write += f'\n{username: <20} {res}'
            file.write(_to_write.strip('\n'))

    # достаёт параметр, а если юзера/параметра нет, установит дефолт, и вернёт
    def get(self, user, param) -> str:
        try:
            return self.data[user][param]
        except KeyError:
            self.data[user] = self._default()
            return self.get(user, param)

    # устанавливает параметр пользователю
    def set(self, user, param, value):
        if user not in self.data:
            self.data[user] = self._default()
        self.data[user][param] = value
        self._save()


# тесты
if __name__ == '__main__':
    us = UserSettings()
    #
    # us.set('jjake', 'panel', 'shown')
    # us.set('bogdan', 'style', 'dark')
    # print()
    print(us.get('asdfa', 'panel'))
    print(us.get('jjake', 'panel'))
    # us.set('asdfa', 'style', 'dark')
    print(us.get('1231', 'style'))