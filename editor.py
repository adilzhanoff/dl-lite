from datetime import datetime
import os


class Editor:
    def __init__(self, code=[]):
        self.__code = code

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    def write_script(self):
        i, line = 1, ''
        while not line.endswith(';'):
            line, i = input(f"{i}: ").replace('\t', '    '), i + 1
            self.__code.append(line + '\n')

        self.__code[-1] = self.code[-1][:-2] + '\n'

    def run_script(self, sign=''):
        try:
            # creates new folder
            os.mkdir(os.getcwd() + "\\Hometasks")
        # if already exists
        except FileExistsError:
            pass
        os.chdir(os.getcwd() + "\\Hometasks")

        current = datetime.now()
        date = str(current.date())
        time = f"{current.hour}:{current.minute}:{current.second}"
        time_sign = ' '.join([date, time, sign])

        with open(f"script ({time_sign}).py") as py:
            py.writelines(self.__code)
        exec(open(f"script ({time_sign}).py").read())

        return os.getcwd() + f"\\script ({time_sign}).py"
