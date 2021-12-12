# TextCloud - система удаленного доступа к базе данных, которая хранит текстовые данные. Реализован контроль доступа к бд. #
## Запуск сервера ##
    python server.py
## Запуск клиента ##
    python client.py
## Для взаимодействия клиента с сервером воспользуйтесь следующими командами: ##
Пример запроса:
* ul
    1. Регистрация: reg login password
    2. Аунтетификация: auth login password
    4. Создание файла: create name text
    5. Чтение файла: read file_id
    6. Изменение файла: update file_id changed_text
    7. Удаление файла: delete id
    8. Показать файлы пользователя: show
    9. Дать доступ: give_access file_id user_id access_type
    10. Забрать доступ: remove_access file_id user_id access_type
