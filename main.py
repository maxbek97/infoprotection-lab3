import os
from User_local import *
from graffic_key import *

def find_user(login, users_list):
    marker = False
    for i in users_list:
        if i.name == login:
            marker = True
            return i
        
    if marker == False:
        print("Пользователь с таким логином не найден")
        return marker
    
def generate_random_key(name):
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
    f.write(name + ": " + "".join(map(str, key_sequence)) + "\n")
    return key_sequence

def int_inputer(text: str, high_bound: int):
    while True:
        answer = input(text)
        try:
            answer = int(answer)
        except (ValueError):
            print("Ошибка выполнения операции")
        else:
            if answer > 0 and answer <= high_bound:
                return answer
            else:
                print("Ошибка выполнения операции. Допустим ввод только натуральных чисел.")



class Task():
    def __init__(self, path = "files/"):
        f = open("keys.txt", 'w')
        f.close()
        self.user_names_examples = ["Ivan", "Boris", "Maxeeb", "Skibidi", "Lol"]
        self.path = path
        self.users_count = int_inputer("Введите кол-во пользователей > ", len(self.user_names_examples))
        self.files_count = int_inputer("Введите кол-во файлов > ", 20)
        self.users_list = [User(self.path, self.user_names_examples[i], generate_random_key(self.user_names_examples[i])) for i in range(0, self.users_count)]
        self.files_list = [File_binder(self.path, i) for i in range(1, self.files_count + 1)]

    # 📌 Функция регистрации нового пользователя
    def register_new_user(self):
        username = input("Введите имя пользователя: ").strip()
        
        print(f"{username}, нарисуйте ваш графический ключ.")
        root = tk.Tk()
        app = GraphicalKeyApp(root, mode="register")
        root.mainloop()

        if app.result:
            key_sequence = app.result  
            with open("keys.txt", "a") as f:
                f.write(f"{username}: {''.join(map(str, key_sequence))}\n")
            print(f"Пользователь {username} успешно зарегистрирован!")
            return User(self.path, username, key_sequence)
        else:
            print("Регистрация отменена.")

    def print_info(self):
        print("Уровни конфиденциальности объектов (О):")
        for i in self.files_list:
            i.print_mandat_access()
        print("\n Уровни допуска пользователей (S):")
        for i in self.users_list:
            i.print_mandat_access()

    def check_user_password(self, correct_key_sequence):
        while True:
            root = tk.Tk()
            app = GraphicalKeyApp(root, correct_key_sequence)
            root.mainloop()
            if app.result is not None:
                return app.result

    def main(self):
        marker = True
        while marker:
            self.print_info()
            a = input('Введите "sign up" для регистрации или продолжить> ')
            if a == "sign up":
                self.users_list.append(self.register_new_user())
            else:
                login = input("Введите имя пользователя: ")
                user = find_user(login, self.users_list)
                if user != False:
                    if self.check_user_password(user.key):
                        print("Идентификация прошла успешно. Добро пожаловать в систему.")
                        print("Перечень доступных объектов: " + ", ".join([x.name for x in self.files_list if x.access_right <= user.mandate_rights]))
                        while True:
                            a = input("Жду ваших указаний > ")
                            if a == "request":
                                file_number = int_inputer("К какому файлу вы хотите осуществить доступ? > ", self.files_count)
                                user.requestfile(self.files_list[file_number - 1])
                            elif a == "read":
                                file_number = int_inputer("Какой файл вы хотите прочитать? > ", self.files_count)
                                self.files_list[file_number - 1].read_file(user)
                            elif a == "write":
                                file_number = int_inputer("В какой файл вы хотите вписать данные? > ", self.files_count)
                                self.files_list[file_number - 1].write_to_file(user)
                            elif a == "quit":
                                print(f"Работа пользователя {user.name} завершена. До свидания")
                                break
                            elif a == "exit":
                                print("Уиа пока")
                                return
                            else:
                                print("Ошибка ввода")
                    else:
                        continue

if __name__ == "__main__":
    task = Task()
    task.main()
