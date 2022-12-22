import sqlite3
from statements import *

class DB ():
    def __init__(self, name) -> None:
        self.con = sqlite3.connect(f"{name}.db")
        self.cur = self.con.cursor()
        #self.cur.execute(create_table_statement)
        # self.execute_cmd(insert_new_user_statement, ('ilja', "poker", 'salt'))
    
    def execute_cmd(self, cmd, args=None) -> None:
        try:
            self.cur.execute(cmd, args)
        except Exception as e:
            print(f'Failed to execute the statement: {cmd}, args: {args}, exception {e}')

    def insert_new_user(self, username: str, master_password_hash: bytes, salt: bytes):
        self.execute_cmd(insert_new_user_statement, (username, master_password_hash, salt))

    def update_user_password(self, username: str, master_password_hash: bytes):
        self.execute_cmd(update_user_password_statement, (username, master_password_hash))

    def update_user_data(self, username: str, encrypted_data: bytes, nonce: bytes):
        self.execute_cmd(update_data_statement, (encrypted_data, nonce, username))

    def select_all_from_user_data(self, username: str):
        self.execute_cmd(select_all_from_user_statement, (username,))
        return self.cur.fetchone()
    
    def check_if_user_exists(self, username: str):
        """ if user exists, it returns true"""
        self.execute_cmd(select_all_from_user_statement, (username,))
        rows = self.cur.fetchall()
        return not len(rows) == 0
    
    def check_content(self):
        sqlite_select_query = """SELECT * from master"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        print(records)
