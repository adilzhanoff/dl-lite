from student import Student
from teacher import Teacher
from database import Database


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
        'key' - defines current proccess
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
            choice != str(i)
            for i in range(1, 5)
        ):
            choice = input(
                "1 - View status\n" +
                "2 - My Teachers\n" +
                "3 - Enroll a new course\n" +
                "4 - Log Out\n"
            )
        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            self.enroll()
            self.menu_student()
        elif choice == '4':
            pass

    def enroll(self):
        self.__cur_user.subjects = self.__data.get_courses(self.__cur_user)
        all_courses = self.__data.all_courses()
        to_enroll = tuple(set(all_courses) - set(self.__cur_user.subjects))

        for i, sub in enumerate(to_enroll):
            print(i, ' '.join(sub[0].split('_')).capitalize(), sep=" - ")

        idx = ''
        while all(
            str(i) != idx
            for i in range(len(to_enroll))

        ):
            idx = input("Enter course ID to enroll: ")

        self.__cur_user.subjects.append(to_enroll[int(idx)])
        self.__data.push_course(self.__cur_user, to_enroll[int(idx)][0])

    def menu_teacher(self):
        print(f"Welcome, {self.__cur_user.name}!")
        choice = ''
        while all(
            [choice != str(i)
             for i in range(1, 8)]
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
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            pass
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
            self.__cur_user.subjects = self.__data.get_courses(
                self.__cur_user
            )
            for i, sub in enumerate(self.__cur_user.subjects):
                print(i + 1, sub, sep=" - ")
