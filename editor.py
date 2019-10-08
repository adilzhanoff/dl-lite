import os


PROJECT_PATH = str(
    'E:\\Documents\\Projects and Scripts\\Python Scripts\\Labs\\dl_lite'
)


class Editor:
    def __init__(self, code):
        self.__code = code
        try:
            os.mkdir(os.getcwd() + "\\Hometasks")
        except FileExistsError:
            pass
        os.chdir(os.getcwd() + "\\Hometasks")

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

    def run_script(self, sign):
        name = f"{sign}.py"
        with open(name, "w") as py:
            py.writelines(self.__code)
        exec(open(name).read())

        os.chdir(PROJECT_PATH)
        return [PROJECT_PATH + "\\Hometasks\\" + name, name]
