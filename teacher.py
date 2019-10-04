from user import User


class Teacher(User):
    def __init__(self, name, surname, subjects={}, grades={}):
        super().__init__(name, surname, subjects, grades)
