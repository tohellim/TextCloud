import sqlite3
from hasher import check_password, hash_password


class DBController():
    def init_db(self):
        global db
        global sql
        db = sqlite3.connect('DataController.db')
        sql = db.cursor()

        db.execute("PRAGMA foreign_keys = 1")

        sql.execute("""CREATE TABLE IF NOT EXISTS users_auth(
        id integer PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        password TEXT NOT NULL
        )""")
        db.commit()

        sql.execute("""CREATE TABLE IF NOT EXISTS data_store(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        text TEXT,
        owner TEXT NOT NULL,
        r_access TEXT,
        w_access TEXT
        )""")
        db.commit()

    def add_user(self, login, password):

        try:
            sql.execute(
                "INSERT INTO users_auth (login, password) VALUES(?, ?)",
                (login, hash_password(password)))
            db.commit()
            return('Регистрация прошла успешно')
        except Exception:
            return('Такой пользователь уже существует')

    def auth_user(self, login, password):
        try:
            sql.execute(
                f"SELECT password FROM users_auth WHERE login = '{login}'")
            dbpass = sql.fetchone()

            #   Авторизован
            if check_password(dbpass[0], password):
                return('Успешный вход')

            #   Не авторизован
            else:
                return('Неверные пароль')

        #   Такого пользователя нет
        except Exception:
            return('Неверный логин')

    def add_file(self, name, owner, text):
        r_access = owner
        w_access = owner
        owner_name = owner + "_" + name
        sql.execute(f"SELECT owner, name FROM data_store WHERE name = '{owner_name}' AND owner = '{owner}'")
        dbowner = sql.fetchall()
        try:
            print(dbowner)
            print(dbowner)
            if str(dbowner[0][1]) == str(owner+"_"+name):
                return('Файл с таким именем уже существует')
        except Exception:
            sql.execute("INSERT INTO data_store (name, text, owner, r_access, w_access) VALUES(?, ?, ?, ?, ?)", (owner_name, text, owner, r_access, w_access))
            db.commit()
            return('Файл создан')

    def read_file(self, name, login):
        sql.execute(f"SELECT text, r_access FROM data_store WHERE name = '{name}'")
        dbfiles = sql.fetchall()
        for dbfile in dbfiles:
            users = str(dbfile[1]).split(',')
            if login in users:
                return str(dbfile[0])
        return('Невозможно прочитать')

    def update_file(self, name, login, text):
        sql.execute(f"SELECT text, w_access, owner FROM data_store WHERE name = '{name}'")
        dbfiles = sql.fetchall()
        for dbfile in dbfiles:
            users = str(dbfile[1]).split(',')
            if login in users:
                sql.execute(f"UPDATE data_store SET text = '{text}' WHERE name = '{name}' AND owner = '{dbfile[2]}'")
                db.commit()
                return ('Файл обновлён')
        return ('Файл не найден')

    def delete_file(self, name, login):
        sql.execute(f"SELECT w_access, owner FROM data_store WHERE name = '{name}'")
        dbfiles = sql.fetchall()
        for dbfile in dbfiles:
            users = str(dbfile[0]).split(',')
            if (login in users) or (login == dbfile[1]):
                sql.execute(f"DELETE FROM data_store WHERE name = '{name}' AND owner = '{dbfile[1]}'")
                db.commit()
                return ('Файл удалён')
        return ('Файл не найден')

    def show_files(self, login):
        files = list()
        sql.execute("SELECT name, r_access, owner FROM data_store")
        dbfiles = sql.fetchall()
        for dbfile in dbfiles:
            users = str(dbfile[1]).split(',')
            if (login in users) or (login == dbfile[2]):
                files.append(dbfile[0])
        if(len(files) > 0):
            return str(files)
        return ('Файлы не найдены')

    def give_access(self, name, owner, access_type, user):
        r_users = ''
        w_users = ''

        sql.execute(f"SELECT login FROM users_auth WHERE login = '{user}'")
        logins = sql.fetchone()
        if user in logins:
            sql.execute(f"SELECT w_access, r_access FROM data_store WHERE name = '{name}' AND owner = '{owner}'")
            users = sql.fetchone()

            rr_users = users[1].split(',')
            ww_users = users[0].split(',')

            if (access_type == 'read'):
                if user in rr_users:
                    r_users = f'{users[1]}'
                    w_users = f'{users[0]}'
                else:
                    r_users = f'{users[1]},{user}'
                    w_users = f'{users[0]}'

            if (access_type == 'update'):
                if user in ww_users:
                    r_users = f'{users[1]}'
                    w_users = f'{users[0]}'
                else:
                    r_users = f'{users[1]},{user}'
                    w_users = f'{users[0]},{user}'

            sql.execute(f"UPDATE data_store SET r_access = '{r_users}', w_access = '{w_users}' WHERE name = '{name}' AND owner = '{owner}'")
            db.commit()
            return(f'Пользователь {user} добавлен')
        else:
            return('Такого пользователя не существует')

    def remove_access(self, name, owner, access_type, user):
        r_users = f'{owner}'
        w_users = f'{owner}'

        sql.execute(f"SELECT login FROM users_auth WHERE login = '{user}'")
        logins = sql.fetchone()
        if user in logins:
            sql.execute(f"SELECT w_access, r_access FROM data_store WHERE name = '{name}' AND owner = '{owner}'")
            users = sql.fetchone()

            rr_users = str(users[1]).split(',')
            ww_users = str(users[0]).split(',')

            if (access_type == 'read'):
                for r_user in rr_users:
                    if (r_user != owner) & (r_user != user):
                        r_users += f',{r_user}'

                for w_user in ww_users:
                    if (w_user != owner) & (w_user != user):
                        w_users += f',{w_user}'

            if (access_type == 'update'):
                for w_user in ww_users:
                    if (w_user != owner) & (w_user != user):
                        w_users += f',{w_user}'
                r_users = f'{users[1]}'

            sql.execute(f"UPDATE data_store SET r_access = '{r_users}', w_access = '{w_users}' WHERE name = '{name}' AND owner = '{owner}'")
            db.commit()
            return(f'Пользователь {user} удалён')
        else:
            return('Такого пользователя не существует')

    def close_db(self):
        db.close()
