import random
from main import find_user
import os
        
class User():
    def __init__(self, path, name, files_count):
        self.path = path
        self.name = name
        self.mandate_rights = random.randint(0, 2)
        self.key = self.generate_random_key()
        self.transfer_rights = [round(random.random()) for i in range(0, files_count)]
        self.readfile_rights = [round(random.random()) for i in range(0, files_count)]
        self.writefile_rights = [round(random.random()) for i in range(0, files_count)]

    def readfile(self, file_number):
        if self.readfile_rights[file_number - 1] == 1:
            f = open(self.path + "file" + str(file_number) + ".txt", "r")
            print(f.read())
            f.close()
        else:
            print("Доступ запрещен")

    def get_intermediate_point(self, a, b):
        intermediate_map = {
            (0, 2): 1, (2, 0): 1, (3, 5): 4, (5, 3): 4, (6, 8): 7, (8, 6): 7,
            (0, 6): 3, (6, 0): 3, (1, 7): 4, (7, 1): 4, (2, 8): 5, (8, 2): 5,
            (0, 8): 4, (8, 0): 4, (2, 6): 4, (6, 2): 4
        }
        return intermediate_map.get((a, b))

    def generate_random_key(self):
        available_indices = list(range(9))
        random.shuffle(available_indices)
        key_length = random.randint(4, 9)
        key_sequence = [available_indices.pop(0)]

        while len(key_sequence) < key_length:
            next_index = random.choice(available_indices)
            last_index = key_sequence[-1]
            if next_index == last_index:
                continue  # Исключаем повторение подряд
            intermediate = self.get_intermediate_point(last_index, next_index)
            if intermediate is not None and intermediate not in key_sequence:
                key_sequence.append(intermediate)
            key_sequence.append(next_index)
            available_indices.remove(next_index)
        f = open("keys.txt", "a")
        f.write(self.name + ": " + "".join(map(str, key_sequence)) + "\n")
        return key_sequence

    def writefile(self, file_number):
        if self.writefile_rights[file_number - 1] == 1:
            f = open(self.path + "file" + str(file_number) + ".txt", "a")
            f.write(input("Вписывайте вашу информацию > "))
            f.close()
        else:
            print("Доступ запрещен")

    def transfer_right(self, file_number, right_type, user_name, users_list):
        if self.transfer_rights[file_number - 1] == 1:
            user = find_user(user_name, users_list)
            if user != False:
                if right_type == "read" and self.readfile_rights[file_number - 1] == 1:
                    user.readfile_rights[file_number - 1] = 1
                elif right_type == "write" and self.writefile_rights[file_number - 1] == 1:
                    user.writefile_rights[file_number - 1] = 1
                elif right_type == "grant":
                    user.transfer_rights[file_number - 1] = 1
                else:
                    print("Отказ выполнения операции.")
            else:
                print("Ошибка выполнения операции. Пользователь с такми именем не найден.")
        else:
            print("Отказ выполнения операции. У вас нет прав для её осуществления.")

    def print_rights_list(self, files_count):
        print("Перечень Ваших прав:")
        for i in range(0, files_count):
            answer = []
            if self.transfer_rights[i] == 0 and self.readfile_rights[i] == 0 and self.writefile_rights[i] == 0:
                answer.append("Полный запрет")
            elif self.transfer_rights[i] == 1 and self.readfile_rights[i] == 1 and self.writefile_rights[i] == 1:
                answer.append("Полный доступ")
            else:
                if self.readfile_rights[i] == 1:
                    answer.append("чтение")
                if self.writefile_rights[i] == 1:
                    answer.append("запись")
                if self.transfer_rights[i] == 1:
                    answer.append("передача")
            print("file" + str(i+1) + ".txt: " + (",".join(answer)).title())

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

    def print_mandat_access(self):
        if self.access_right == 0:
            print(f"{self.name}: Открытые данные")
        elif self.access_right == 1:
            print(f"{self.name}: Секретно")
        elif self.access_right == 2:
            print(f"{self.name}: Совершенно секретно")

