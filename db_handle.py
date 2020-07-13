from pymysql import connect
from pymysql.cursors import DictCursor


class Database:
    def __init__(self, host, user, password, db, charset='utf8mb4'):
        self.connection = connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=DictCursor
        )

    def query(self, sql, *params):
        with self.connection:
            self.cur = self.connection.cursor()
            return self.cur.execute(sql, *params)


class Quote:

    def __init__(self, db):
        self.connected = db

    def get_one(self, quote_id):
        sql = "select * from quotes where quote_id = %s"
        self.connected.query(sql, quote_id)

        return self.connected.cur.fetchone()

    def get_all(self):
        sql = "select quote_id, message_text from quotes"
        self.connected.query(sql)

        return self.connected.cur.fetchall()

    def save(self, message):
        sql = "insert into quotes (message_id, from_username, from_name, from_lastname, message_date_time, message_text) values (%s, %s, %s, %s, %s, %s)"
        self.connected.query(sql, (
            message.message_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.date,
            message.text
        ))
        self.connected.connection.commit()

        return self.last_index()

    def get_by_message_id(self, message_id):
        sql = "select * from quotes where message_id = %s"
        self.connected.query(sql, message_id)

        return self.connected.cur.fetchone()

    def delete(self, quote_id):
        sql = "delete from quotes where quote_id = %s"
        self.connected.query(sql, quote_id)
        self.connected.connection.commit()

        return True

    def last_index(self):
        sql = "select last_insert_id()"
        self.connected.query(sql)

        return self.connected.cur.fetchone()['last_insert_id()']

    def random(self):
        sql = "select * from quotes order by rand() limit 1"
        self.connected.query(sql)

        return self.connected.cur.fetchone()
