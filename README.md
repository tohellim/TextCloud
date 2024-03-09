# TextCloud - учеьный проект для изучения матричной схемы доступа к данным #
## Запуск сервера ##
    python server.py
## Запуск клиента ##
    python client.py
## Для взаимодействия клиента с сервером воспользуйтесь следующими командами: ##
Примеры запросов:

    * Регистрация: reg login password
    * Аунтетификация: auth login password
    * Создание файла: create name text
    * Чтение файла: read file_id
    * Изменение файла: update file_id changed_text
    * Удаление файла: delete id
    * Показать файлы пользователя: show
    * Дать доступ: give_access file_id user_id access_type
    * Забрать доступ: remove_access file_id user_id access_type
