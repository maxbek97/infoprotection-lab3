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
        self.users_list = [User(self.path, self.user_names_examples[i], self.files_count) for i in range(0, self.users_count)]
        self.files_list = [File_binder(self.path, i) for i in range(1, self.files_count + 1)]
        # Очистка файла keys


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
        self.print_info()
        marker = True
        while marker:
            login = input("Введите имя пользователя: ")
            user = find_user(login, self.users_list)
            if user != False:
                if self.check_user_password(user.key):
                    print("Идентификация прошла успешно. Добро пожаловать в систему.")
                    print("Перечень доступных объектов: " + ", ".join([x.name for x in self.files_list if x.access_right <= user.mandate_rights]))
                    while True:
                        a = input("Жду ваших указаний > ")
                        if a == "request":
                            file_number = int_inputer("К какому файлу вы хотите осуществит доступ? > ", self.files_count)
                            user.requestfile(self.files_list[file_number - 1])
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
