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

    def get_one_quote(self, connected, quote_number):
        sql = "select * from quotes where quote_id = %s"
        connected.query(sql, quote_number)
        return connected.cur.fetchone()

    def get_all(self, connected):
        sql = "select quote_id, message_text from quotes"
        connected.query(sql)
        return connected.cur.fetchall()

    def post_quote(self, connected, message_id, from_username, from_name, from_lastname, message_date_time,
                   message_text):
        sql = "insert into quotes (message_id, from_username, from_name, from_lastname, message_date_time, message_text) values (%s, %s, %s, %s, %s, %s)"
        connected.query(sql, (message_id, from_username, from_name, from_lastname, message_date_time, message_text))
        connected.connection.commit()
        return True

    def delete_quote(self, connected, quote_id):
        sql = "delete from quotes where quote_id = %s"
        connected.query(sql, quote_id)
        connected.connection.commit()
        return True
