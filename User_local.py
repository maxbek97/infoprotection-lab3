import random
from main import find_user
import os
        
class User():
    def __init__(self, path, name, files_count):
        self.path = path
        self.name = name
        self.mandate_rights = random.randint(0, 2)
        self.key = self.generate_random_key()

    # Генерация корректного ключа
    def generate_random_key(self):
        VALID_MOVES = {
        0: {1, 3, 4, 5, 7}, 
        1: {0, 2, 3, 4, 5, 6, 8}, 
        2: {1, 3, 4, 5, 7}, 
        3: {0, 1, 2, 4, 6, 7, 8}, 
        4: {0, 1, 2, 3, 5, 6, 7, 8}, 
        5: {0, 1, 2, 4, 6, 7, 8}, 
        6: {1, 3, 4, 5, 7}, 
        7: {0, 2, 3, 4, 5, 6, 8}, 
        8: {1, 3, 4, 5, 7}
    }
        key_length = random.randint(4, 7)  # Длина ключа
        key_sequence = [random.randint(0, 8)]  # Начинаем с случайной точки

        while len(key_sequence) < key_length:
            last = key_sequence[-1]
            possible_moves = list(VALID_MOVES[last])  # Получаем список доступных точек
            random.shuffle(possible_moves)

            for next_point in possible_moves:
                if next_point != key_sequence[-1]:  # Запрещаем повтор подряд
                    key_sequence.append(next_point)
                    break
        f = open("keys.txt", "a")
        f.write(self.name + ": " + "".join(map(str, key_sequence)) + "\n")
        return key_sequence

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

