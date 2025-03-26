import tkinter as tk
from tkinter import messagebox
import math

class GraphicalKeyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Key Authentication")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.points = []
        self.grid_points = []
        self.correct_key_indices = [0, 2, 4, 6, 8]  # Пример последовательности точек для ключа

        # Создание сетки из 9 точек
        self.create_grid()

        # Отображение правильных точек на полотне
        for index in self.correct_key_indices:
            point = self.grid_points[index]
            self.canvas.create_oval(point[0]-10, point[1]-10, point[0]+10, point[1]+10, fill="blue")

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

        self.check_button = tk.Button(root, text="Check Key", command=self.check_key)
        self.check_button.pack()

    def create_grid(self):
        # Создание сетки 3x3 точек по центру
        start_x, start_y = 100, 100
        spacing = 100
        for i in range(3):
            for j in range(3):
                x = start_x + j * spacing
                y = start_y + i * spacing
                self.grid_points.append((x, y))
                self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="gray")

    def start_drawing(self, event):
        self.points.append((event.x, event.y))

    def draw(self, event):
        if self.points:
            x0, y0 = self.points[-1]
            x1, y1 = event.x, event.y
            self.canvas.create_line(x0, y0, x1, y1, fill="black", width=2)
            self.points.append((x1, y1))

    def end_drawing(self, event):
        self.points.append((event.x, event.y))

    def check_key(self):
        if self.is_key_correct():
            messagebox.showinfo("Success", "Access Granted!")
        else:
            messagebox.showerror("Failure", "Access Denied!")
        self.points = []
        self.canvas.delete("all")
        # Перерисовка сетки и правильных точек после очистки
        self.create_grid()
        for index in self.correct_key_indices:
            point = self.grid_points[index]
            self.canvas.create_oval(point[0]-10, point[1]-10, point[0]+10, point[1]+10, fill="blue")

    def is_key_correct(self):
        # Проверяем, проходит ли линия через все правильные точки в правильном порядке
        current_index = 0
        for index in self.correct_key_indices:
            point = self.grid_points[index]
            found = False
            for p in self.points:
                if self.is_close(p, point):
                    if current_index == self.correct_key_indices.index(index):
                        found = True
                        current_index += 1
                        break
            if not found:
                return False
        return True

    def is_close(self, point1, point2, tolerance=30):
        distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return distance < tolerance

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalKeyApp(root)
    root.mainloop()
