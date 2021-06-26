import sqlite3
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.username_cur = self.conn.cursor()
        self.password_cur = self.conn.cursor()
        self.email_cur = self.conn.cursor()
        self.logged_in_id = None
    def connect(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, email text)")
        self.conn.commit()
    def get_id(self, username):
        self.cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = self.cur.fetchall()
        return row[0][0]
    def insert(self,username, password, email):

        self.username_cur.execute("SELECT username FROM users")
        usernames =self.username_cur.fetchall()
        for i in usernames:
            if i[0] == username:
                return False, "username"
        self.password_cur.execute("SELECT password FROM users")
        passwords = self.password_cur.fetchall()
        for i in passwords:
            if i[0] == password:
                return False, "password"
        self.email_cur.execute("SELECT email FROM users")
        emails = self.email_cur.fetchall()
        for i in emails:
            if i[0] == email:
                return False, "email"
        self.cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?) ", (username, password, email))  
        self.conn.commit()
        return True, "signed up"
    def view(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows
    def delete(self,id):
        self.cur.execute("DELETE FROM users WHERE id = ?", (id,))
        self.conn.commit()

    def update_pwd(self,new_password, username):
        self.password_cur.execute("SELECT password FROM users")
        passwords = self.password_cur.fetchall()
        for i in passwords:
            if i[0] == new_password:
                return False
        self.cur.execute("UPDATE users SET password = ? WHERE username=?", (new_password, username))
        self.conn.commit()
        return True
    def user_exists(self,username, password):
        #self.cur.execute("SELECT * FROM users WHERE username=? AND password =?", (username, password))
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        for row in rows:
            if list(row)[1] == username and list(row)[2] == password:
                self.logged_in_id = list(row)[0]
                return True
        return False
    def username_exists(self, username):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        for row in rows:
            if list(row)[1] == username:
                return True
        return False
    def pwd_exists(self, password):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        for row in rows:
            if list(row)[2] == password:
                return True
        return False

    def __del__(self):
        self.conn.close()

class Tasks:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cur = self.conn.cursor()
    def connect(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS tasks  (id INTEGER PRIMARY KEY, user_id integer, task text, hour text, minute text, day text, month text, year text)")
        self.conn.commit()
    def insert(self, user_id, task, hour, minute, day, month, year):
        self.cur.execute("INSERT INTO tasks VALUES(NULL, ?,?,?,?,?,?,?)", (user_id, task, hour, minute, day, month, year))  
        self.conn.commit()
    def todays_tasks(self,user_id, day, month, year):
        self.cur.execute("SELECT * FROM tasks WHERE user_id=? AND day=? AND month=? AND year=?", (user_id,day, month, year))
        rows = self.cur.fetchall()
        return rows
    def view(self, user_id):
        self.cur.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        rows = self.cur.fetchall()
        return rows
    def delete_task(self, user_id, task, hour, minute, day, month, year):
        self.cur.execute("DELETE FROM tasks WHERE user_id=? AND task=? AND hour=? AND minute=? AND day=? AND month=? AND year=?", (user_id, task, hour, minute, day, month, year))
        self.conn.commit()
    def delete_task_by_id(self, user_id, id):
        self.cur.execute("DELETE FROM TASKS WHERE user_id=? AND id=?",(user_id, id))
        self.conn.commit()
    def delete_all_tasks(self, user_id):
        self.cur.execute("DELETE FROM tasks WHERE user_id=?", (user_id,))
        self.conn.commit()

    def delete_table(self):
        self.cur.execute("DROP TABLE tasks")
        self.conn.commit()
    # def update(self, user_id, id):
    def get_id(self, user_id, task, hour, minute, day, month, year):
        self.cur.execute("SELECT id FROM tasks WHERE user_id=? AND task=? AND hour=? AND minute=? AND day=? AND month=? AND year=?", (user_id, task, hour, minute, day, month, year))
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows[0][0]
    def update(self, user_id, id, task, hour, minute, day, month, year):
        self.cur.execute("UPDATE tasks SET task=? AND hour=? AND minute=? AND day=? AND month=? AND year=? WHERE id=? AND user_id=?", (task, hour, minute, day, month, year, id, user_id))
        self.conn.commit()
    def __del__(self):
        self.conn.close()

db = Database()

# tasks = Tasks()
# tasks.connect()
# tasks.insert('do that thing', '23-11-221')
# print(tasks.view())
# tasks = Tasks()
# tasks.delete_task(None)
# db = Database()
# print(db.view())
# tasks = Tasks()
# tasks.connect()
# print(tasks.get_id(6, 'go to school', '09', '00', '01', '05', '2021'))
# print("all tasks:", tasks.view(6))
# print("today's tasks: ", tasks.todays_tasks(6, "30", "04", "2021"))
# print("tomorrow's tasks: ", tasks.todays_tasks(6, "01", "05", "2021"))
# print(tasks.view(6))
# tasks.delete_table()
