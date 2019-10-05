class User:
    def __init__(self, name, surname, subjects=[], grades={}):
        self.__name = name
        self.__surname = surname
        self.__subjects = subjects
        self.__grades = grades

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        self.__surname = surname

    @property
    def subjects(self):
        return self.__subjects

    @subjects.setter
    def subjects(self, subjects):
        self.__subjects = subjects

    @property
    def grades(self):
        return self.__grades

    @grades.setter
    def grades(self, grades):
        self.__grades = grades
