from student import Student
from teacher import Teacher
from database import Database
import pandas as pd


class Menu:
    """
    class that provides a menu for
    a user to interact with the programme
    """
    def __init__(self):
        self.__data = Database()
        self.__cur_user = None

    def run(self):
        choice = ''
        while choice != '3' and '1' != choice != '2':
            choice = input(
                "1 - Log In\n" +
                "2 - Sign Up\n" +
                "3 - Exit\n"
            )

        if choice == '1' or choice == '2':
            self.auth_user(key=("up", "in")[choice == '1'])
        else:
            pass

    def auth_user(self, key="in"):
        """
        'key' - defines now proccess
            "in" - for logging in
            "up" - for signing up
        """
        name = input("Enter your name: ").lower()
        surname = input("Enter your surname: ").lower()
        role = ''
        while 't' != role != 's':
            role = input("Are you a teacher or a student? (t/s): ").lower()
        # reference to a certain class
        role = (Student, Teacher)[role == 't']
        # temporary object of the certain class
        temp = role(name, surname)

        if self.__data.is_exist(role(name, surname)):
            # user exists,
            # logging in
            if key == "in":
                print("You are logged in.")
                self.__cur_user = temp
                if isinstance(self.__cur_user, Teacher):
                    self.menu_teacher()
                else:
                    self.menu_student()
            # signging up
            elif key == "up":
                print("Such user has already been registered.")
            self.run()
        else:
            # doesn't exist,
            # logging in
            if key == "in":
                print("Such user has not been found.")
            # signing up
            elif key == "up":
                self.__data.push_user(temp)
            self.run()

    def menu_student(self):
        print(f"Welcome, {self.__cur_user.name}!")
        choice = ''
        while all(
            [choice != str(i) for i in range(1, 5)]
        ):
            choice = input(
                "1 - View status\n" +
                "2 - My Teachers\n" +
                "3 - Enroll a new course\n" +
                "4 - Log Out\n"
            )

        if choice == '1':
            self.view_status()
            self.menu_student()
        elif choice == '2':
            self.show_teachers()
            self.menu_student()
        elif choice == '3':
            self.enroll()
            self.menu_student()
        elif choice == '4':
            pass

    def view_status(self):
        self.__cur_user.grades = self.__data.get_grades(self.__cur_user)
        grades = self.__cur_user.grades.copy()
        grades = ((k, v) for k, v in grades.items())
        table = pd.DataFrame(
            grades, columns=("Course", "Grade"), index=(1, 2)
        ).T
        print(table.T)

    def show_teachers(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)
        tchrs = self.__cur_user.subjects
        if tchrs != []:
            tchrs = [
                ' '.join(elem[0].split('_')[:2]) for elem in tchrs
            ]
            tchrs = {
                each[:each.index(' ')].capitalize() +
                ' ' + each[each.index(' ') + 1:].capitalize()
                for each in tchrs
            }
            print("My Teachers: ")
            for i, tchr in enumerate(tchrs):
                print(i + 1, tchr, sep=" - ")
        else:
            print("Your teacher list is empty.")

    def enroll(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)
        all_courses = self.__data.all_courses()
        to_enroll = tuple(set(all_courses) - set(self.__cur_user.subjects))

        for i, sub in enumerate(to_enroll):
            print(i, ' '.join(sub[0].split('_')).capitalize(), sep=" - ")

        idx = ''
        while all(
            [str(i) != idx for i in range(len(to_enroll))]

        ):
            idx = input("Enter course ID to enroll: ")

        self.__cur_user.subjects.append(to_enroll[int(idx)])
        self.__data.push_course(self.__cur_user, to_enroll[int(idx)][0])

    def menu_teacher(self):
        print(f"Welcome, {self.__cur_user.name}!")
        choice = ''
        while all(
            [choice != str(i) for i in range(1, 8)]
        ):
            choice = input(
                "1 - Add a new course\n" +
                "2 - See courses you lead\n" +
                "3 - Mark student(s)\n" +
                "4 - Add student(s) to course\n" +
                "5 - Remove student(s) from course\n" +
                "6 - See the stastics\n" +
                "7 - Log out\n"
            )

        if choice == '1':
            self.add_course()
            self.menu_teacher()
        elif choice == '2':
            self.show_courses(self.__cur_user)
            self.menu_teacher()
        elif choice == '3':
            self.mark_student()
            self.menu_teacher()
        elif choice == '4':
            self.add_student()
            self.menu_teacher()
        elif choice == '5':
            self.remove_student()
            self.menu_teacher()
        elif choice == '6':
            self.show_stat()
            self.menu_teacher()
        elif choice == '7':
            pass

    def add_course(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)

        while True:
            name = '_'.join(input("Enter the course name: ").lower().split())
            if name in self.__cur_user.subjects and name != "name":
                print("Such course already exists.")
            else:
                self.__cur_user.subjects.append(name)
                self.__data.push_course(self.__cur_user, name)
                print(
                    f"{name.capitalize()} course has been succesfully added."
                )
                break

    def show_courses(self, usr):
        if isinstance(usr, Teacher):
            self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)
            for i, sub in enumerate(self.__cur_user.subjects):
                print(i + 1, sub, sep=" - ")

    def mark_student(self):
        self.__cur_user.grades = self.__data.get_stat(self.__cur_user)
        grades = self.__cur_user.grades.copy()

        if any(
            [grades[key] != {}
             for key in grades]
        ):
            for i, sub in enumerate(grades.keys()):
                print(i, sub, sep=" - ")

            idx = ''
            while all(
                [str(j) != idx for j in range(i + 1)]
            ):
                idx = input("Enter course ID: ")

            course = tuple(grades.keys())[int(idx)]
            info = grades[course]
            for i, stud in enumerate(info):
                if info[stud] is not None:
                    print(i, stud, sep=" - ")

            jdx = ''
            while all(
                [str(j) != jdx for j in range(i + 1)]
            ):
                jdx = input("Enter student ID: ")

            while True:
                try:
                    mark = float(input("Enter new mark: "))
                    break
                except ValueError:
                    print("Incorrect mark entered, try again!")

            init = tuple(info.keys())[int(jdx)]
            surname = init[:init.index('_')]
            name = init[init.index('_') + 1:]

            self.__data.set_mark(
                self.__cur_user, surname,
                name, course, mark
            )

    def add_student(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)

        if self.__cur_user.subjects != []:
            for i, sub in enumerate(self.__cur_user.subjects):
                print(i, sub, sep=" - ")

            idx = ''
            while all(
                [str(j) != idx for j in range(i + 1)]
            ):
                idx = input("Enter course ID: ")

            course = self.__cur_user.subjects[int(idx)]
            new = tuple(self.__data.new_students(self.__cur_user, course))

            if new != ():
                for i, stud in enumerate(new):
                    print(i, stud, sep=" - ")

                idx = ''
                while all(
                    [str(j) != idx for j in range(i + 1)]
                ):
                    idx = input("Enter student ID to add: ")

                self.__data.push_student(
                    self.__cur_user,
                    new[int(idx)][:new[int(idx)].index('_')],
                    new[int(idx)][new[int(idx)].index('_') + 1:],
                    course
                )
            else:
                print("No new students to add for this course.")
        else:
            print("You lead no courses, add some through menu.")

    def remove_student(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)

        if self.__cur_user.subjects != []:
            for i, sub in enumerate(self.__cur_user.subjects):
                print(i, sub, sep=" - ")

            idx = ''
            while all(
                [str(j) != idx for j in range(i + 1)]
            ):
                idx = input("Enter course ID: ")

            course = self.__cur_user.subjects[int(idx)]
            now = tuple(self.__data.new_students(
                self.__cur_user, course,
                key=False
            ))

            if now != ():
                for i, stud in enumerate(now):
                    print(i, stud, sep=" - ")

                idx = ''
                while all(
                    [str(j) != idx for j in range(i + 1)]
                ):
                    idx = input("Enter student ID: ")

                self.__data.pop_student(
                    self.__cur_user,
                    now[int(idx)][:now[int(idx)].index('_')],
                    now[int(idx)][now[int(idx)].index('_') + 1:],
                    course
                )
            else:
                print("No students attend this course.")
        else:
            print("You lead no courses, add some through menu.")

    def show_stat(self):
        table = pd.DataFrame(self.__cur_user.grades)
        print(table)
