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
                # TODO show menu function
            # signging up
            elif key == "up":
                print("Such user has already been registered.")
                self.run()
        else:
            # doesn't exist,
            # logging in
            if key == "in":
                print("Such user has not been found.")
                self.run()
            # signing up
            elif key == "up":
                self.__data.push_user(temp)
                self.run()
