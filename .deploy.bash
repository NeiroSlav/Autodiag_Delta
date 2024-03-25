#!/bin/bash

pip install flask==3.0.2 paramiko==3.4.0
pip install requests==2.31.0 regex

mkdir log
touch init/user_settings.txt
touch connections/personal_data.py

echo "switch_login = логин свитча" >> connections/personal_data.py
echo "switch_password = пароль свитча" >> connections/personal_data.py
echo "tolerance_login = логин толеранса" >> connections/personal_data.py
echo "tolerance_password = пароль толеранса" >> connections/personal_data.py

echo && echo
echo 'заполните файл connections/personal_data.py'
echo 'установите системную утилиту fping'
echo && echo
