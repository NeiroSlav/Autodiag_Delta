ОПИСАНИЕ:

Autodiag_Delta - одностраничное веб-приложение, архитектура VMC.
Проект создан для автоматизации и упрощения работы техподдержки.
Приложение полностью автоматизирует базовые обращения к свитчам,
сравнивает результаты с нормой, и комментирует ошибки в ответах.
Позволяет отправлять пинг на абонентские ip и сканировать порты.
Анализирует корректность флатов dhcp и доступность оборудования.

Поддерживается следующее оборудование:
Dlink, Zyxel, Bdcom, Foxgate, Raisecom, Ubiquiti



СТРУКТУРА:

Бизнес-логика проекта вынесена в библиотеку connections,
которая позволяет подключаться к оборудованию по telnet.
Библиотека может быть использована отдельно вне проекта.

За пределами connections реализованы следующие системы контроля:
-система по структурированию и валидации входных данных из gcdb;
-система создания, поддержки и удаления токенов открытых сессий;
-система контроля утечек памяти серверной части (только из веб);
-система логирования действий токенов юзеров (файлами и из веб).



ДЕПЛОЙ:

Автоматическое развёртывание не реализовано, есть полуавтомат:
-после клона проекта нужно создать venv, и сразу войти в него;
-выполнить в корне проекта файл deploy.bash, он настроит venv;
-внести данные для логина в файл connections/personal_data.py;
-установить системную утилиту fping любым пакетным менеджером;
-запустить файл main.py. Если нужно, поднять любой веб-сервер.