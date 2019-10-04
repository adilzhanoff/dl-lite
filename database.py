import sqlite3 as sql
from user import User
from student import Student
import os


class Database:
    def __init__(self):
        self.__db = None
        self.__db_name = "dl_data.db"

    def is_exist(self, usr):
        """
        checks if 'usr' object
        exists in database
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            table_name = (
                f"{usr.name}_{usr.surname}_" +
                f"{('t', 's')[isinstance(usr, Student)]}",
            )
            # returns table with 'table_name' as a tuple in list
            table = cur.execute(
                """
                SELECT
                    name
                FROM
                    sqlite_master
                WHERE
                    type='table' and
                    name=?
                """, table_name
            ).fetchall()

            if table_name in table:
                return True
            else:
                return False

    def push_user(self, usr):
        """
        adds new table of 'usr'
        object to the database
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            table_name = (
                f"{usr.name}_{usr.surname}_" +
                f"{('t', 's')[isinstance(usr, Student)]}"
            )
            # certain 1st column name depending on whom to add
            column_name = ("Name", "Course")[isinstance(usr, Student)]
            # creates table with given table and column name
            cur.execute(
                """
                CREATE TABLE """ + table_name + """ (
                    """ + column_name + """ text
                )
                """
            )
