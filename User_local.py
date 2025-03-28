import random
from main import find_user
import os
        
class User():
    def __init__(self, path, name, key):
        self.path = path
        self.name = name
        self.mandate_rights = random.randint(0, 2)
        self.key = key

    def requestfile(self, file):
        if self.mandate_rights >= file.access_right:
            print("Операция прошла успешно")
        else:
            print("Отказ выполнения операции. Недостаточно прав.")

    def print_mandat_access(self):
        if self.mandate_rights == 0:
            print(f"{self.name}: Открытые данные")
        elif self.mandate_rights == 1:
            print(f"{self.name}: Секретно")
        elif self.mandate_rights == 2:
            print(f"{self.name}: Совершенно секретно")


class File_binder():
    def __init__(self, path, file_number):
        self.path = path
        self.name = self.path + "file" + str(file_number) + ".txt"
        self.access_right = random.randint(0, 2)
        try:
            os.remove(self.name)
        except:
            pass
        f = open(self.name, 'w')
        f.write("Hello again. There is file " + self.name)
        f.close()

    def read_file(self, user):
        if user.mandate_rights >= self.access_right:
            f = open(self.name, "r")
            for line in f:
                print(line)
            f.close()
            print("Операция завершена успешно.")
        else:
            print("Отказ выполнения операции. Пользователь с низким уровнем доступа не может читать секретные файлы.")

    def write_to_file(self, user):
        if user.mandate_rights <= self.access_right:
            f = open(self.name, "a")
            f.write(input("type > "))
            f.close()
            print("Операция завершена успешно.")
        else:
            print("Отказ выполнения операции. Пользователь с высоким уровнем доступа не может записывать в открытые файлы.")

    def print_mandat_access(self):
        if self.access_right == 0:
            print(f"{self.name}: Открытые данные")
        elif self.access_right == 1:
            print(f"{self.name}: Секретно")
        elif self.access_right == 2:
            print(f"{self.name}: Совершенно секретно")

