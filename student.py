from user import User


class Student(User):
    def __init__(self, name, surname, subjects=[], grades={}, tasks={}):
        super().__init__(name, surname, subjects, grades, tasks)
