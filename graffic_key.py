import tkinter as tk
from tkinter import messagebox
import math
import random

class Point:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def is_close(self, x, y, tolerance=30):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) < tolerance

class GraphicalKeyApp:
    def __init__(self, root, correct_sequence):
        self.root = root
        self.root.title("Graphical Key Authentication")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.points = []  # Список пройденных точек
        self.grid_points = []  # Список всех точек сетки
        self.create_grid()
        self.correct_key_sequence = correct_sequence  # Генерация случайного ключа

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

        self.result = None

    def create_grid(self):
        start_x, start_y = 100, 100
        spacing = 100
        self.grid_points = []
        index = 0
        for i in range(3):
            for j in range(3):
                x = start_x + j * spacing
                y = start_y + i * spacing
                self.grid_points.append(Point(index, x, y))
                self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="gray")
                index += 1

    def generate_random_key(self):
        available_indices = list(range(9))
        random.shuffle(available_indices)
        key_length = random.randint(4, 9)  # Длина ключа от 4 до 9 точек
        key_sequence = [available_indices.pop(0)]

        while len(key_sequence) < key_length:
            next_index = available_indices.pop(0)
            last_index = key_sequence[-1]
            intermediate = self.get_intermediate_point(last_index, next_index)
            if intermediate is None or intermediate in key_sequence:
                key_sequence.append(next_index)
            else:
                key_sequence.append(intermediate)
                key_sequence.append(next_index)
        return key_sequence

    def start_drawing(self, event):
        self.points = []
        self.canvas.delete("lines")
        self.add_point(event.x, event.y)

    def draw(self, event):
        if self.points:
            self.add_point(event.x, event.y)

    def end_drawing(self, event):
        self.add_point(event.x, event.y)
        self.check_key()

    def add_point(self, x, y):
        for point in self.grid_points:
            if point.is_close(x, y):
                if not self.points or self.points[-1].index != point.index:
                    last_point = self.points[-1] if self.points else None
                    self.points.append(point)
                    if last_point:
                        self.add_intermediate_points(last_point, point)
                        self.canvas.create_line(last_point.x, last_point.y, point.x, point.y, fill="black", width=2, tags="lines")
                break

    def add_intermediate_points(self, start, end):
        mid_x = (start.x + end.x) // 2
        mid_y = (start.y + end.y) // 2
        for point in self.grid_points:
            if point.index != start.index and point.index != end.index and point.x == mid_x and point.y == mid_y:
                if point not in self.points:
                    self.points.insert(-1, point)
                    self.canvas.create_line(start.x, start.y, point.x, point.y, fill="black", width=2, tags="lines")
                    self.canvas.create_line(point.x, point.y, end.x, end.y, fill="black", width=2, tags="lines")
                break

    def check_key(self):
        entered_sequence = [p.index for p in self.points]
        print("Entered sequence:", entered_sequence)  # Вывод введенной последовательности
        if entered_sequence == self.correct_key_sequence:
            messagebox.showinfo("Success", "Access Granted!")
            self.result = True
            self.root.destroy()
        else:
            messagebox.showerror("Failure", "Access Denied!")
            self.points = []
            self.canvas.delete("lines")

    def on_close(self):
        self.result = False
        self.root.destroy()
