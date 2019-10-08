import sqlite3 as sql
from user import User
from student import Student
import os


class Database:
    def __init__(self):
        self.__db = None
        self.__db_name = "dl_data.db"

        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS all_courses (
                    Name text,
                    UNIQUE(Name)
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS all_students (
                    Name text,
                    UNIQUE(Name)
                )
                """
            )

    def is_exist(self, usr):
        """
        checks if 'usr' object
        exists in database
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            table_name = (
                f"{usr.surname}_{usr.name}_" +
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
                f"{usr.surname}_{usr.name}_" +
                f"{('t', 's')[isinstance(usr, Student)]}"
            )
            if isinstance(usr, Student):
                cur.execute(
                    """
                    CREATE TABLE """ + table_name + """ (
                        Course text,
                        Grade real,
                        UNIQUE(Course)
                    )
                    """
                )
                cur.execute(
                    """
                    INSERT INTO all_students (Name)
                    VALUES ('""" +
                    f"{usr.surname}_{usr.name}" +
                    """')
                    """
                )
            else:
                cur.execute(
                    """
                    CREATE TABLE """ + table_name + """ (
                        Name text,
                        UNIQUE(Name)
                    )
                    """
                )

    def all_courses(self):
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            courses = cur.execute(
                """
                SELECT * FROM all_courses
                """
            ).fetchall()
        return courses

    def get_courses(self, usr):
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            if not isinstance(usr, Student):
                courses = cur.execute(
                    """
                    PRAGMA table_info('""" +
                    f"{usr.surname}_{usr.name}_t" +
                    """')
                    """
                ).fetchall()
                courses = [col[1] for col in courses[1:]]
            else:
                courses = cur.execute(
                    """
                    SELECT Course FROM '""" +
                    f"{usr.surname}_{usr.name}_s" +
                    """'
                    """
                ).fetchall()
        return courses

    def push_course(self, usr, name):
        if not isinstance(usr, Student):
            with sql.connect(self.__db_name) as self.__db:
                cur = self.__db.cursor()
                cur.execute(
                    """
                    ALTER TABLE `""" +
                    f"{usr.surname}_{usr.name}_t" +
                    """` ADD `""" +
                    f"{name}" +
                    """` real
                    """
                )
                cur.execute(
                    """
                    INSERT INTO all_courses (Name)
                    VALUES ('""" +
                    f"{usr.surname}_{usr.name}" +
                    f"_{name}" +
                    """')
                    """
                )
        else:
            with sql.connect(self.__db_name) as self.__db:
                cur = self.__db.cursor()
                tchr_name = str(
                    name[:name.index('_', name.index('_') + 1, -1)] + "_t"
                )
                course = name[len(tchr_name) - 1:]
                cur.execute(
                    """
                    INSERT OR IGNORE INTO """ +
                    tchr_name +
                    """ (Name) VALUES ('""" +
                    f"{usr.surname}_{usr.name}" + """')"""
                )
                cur.execute(
                    """
                    UPDATE """ +
                    tchr_name +
                    """ SET '""" +
                    course +
                    """' = 0 WHERE Name = '""" +
                    f"{usr.surname}_{usr.name}'"
                )
                cur.execute(
                    """
                    INSERT OR IGNORE INTO """ +
                    f"{usr.surname}_{usr.name}_s" +
                    """ (Course, Grade) VALUES ('""" +
                    name + """', 0)
                    """
                )

    def new_students(self, usr, name, key=True):
        """
        if key = True, returns students that can be enrolled
        on course 'name' of teacher 'usr'
        else, returns students that attend
        the 'name' course of the teacher 'usr'
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            students = cur.execute(
                """
                SELECT
                    Name
                FROM
                    """ +
                f"{usr.surname}_{usr.name}_t" +
                """ WHERE `""" +
                name + """` IS NOT NULL"""
            ).fetchall()
            students = {
                elem[0] for elem in students
            }
            all_students = cur.execute(
                """
                SELECT
                    *
                FROM
                    all_students
                """
            ).fetchall()
            all_students = {
                elem[0] for elem in all_students
            }
            if key:
                return all_students - students
            else:
                return students

    def push_student(self, tchr, surname, name, course):
        """
        adds student with 'surname' and 'name'
        to the 'course' of the 'tchr'
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            cur.execute(
                """
                INSERT OR IGNORE INTO """ +
                f"{tchr.surname}_{tchr.name}_t" +
                """ (Name) VALUES ('""" +
                f"{surname}_{name}" +
                """')"""
            )
            cur.execute(
                """
                INSERT OR IGNORE INTO """ +
                f"{surname}_{name}_s" +
                """ (Course, Grade)
                VALUES (""" +
                f"'{tchr.surname}_{tchr.name}_{course}'" + """, 0)"""
            )
            cur.execute(
                """
                UPDATE """ +
                f"{tchr.surname}_{tchr.name}_t" +
                """ SET '""" +
                course + """' = 0
                WHERE Name = '""" +
                f"{surname}_{name}'"
            )

    def course_students(self, tchr, course):
        """
        returns all students attending
        the 'course' of 'tchr'
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            students = cur.execute(
                """
                SELECT
                    Name
                FROM
                    """ +
                f"{tchr.surname}_{tchr.name}_t" +
                """ WHERE `""" +
                course + """` IS NOT NULL
                """
            )

    def pop_student(self, tchr, surname, name, course):
        """
        removes student with 'surname' and 'name'
        from the 'course' of the 'tchr'
        """
        with sql.connect(self.__db_name) as self.__db:
            cur = self.__db.cursor()
            cur.execute(
                """
                UPDATE """ +
                f"{tchr.surname}_{tchr.name}_t" +
                """ SET `""" +
                course +
                """` = NULL
                WHERE Name = '""" +
                f"{surname}_{name}'"
            )
            cur.execute(
                """
                DELETE FROM """ +
                f"{surname}_{name}_s" +
                """ WHERE Course = '""" +
                f"{tchr.surname}_{tchr.name}_{course}'"
            )

    def update_student(std):
        pass
