# gui.py
import tkinter as tk
from tkinter import ttk
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from utils.maze import generate_maze
from analysis.performance import calculate_path_quality
import time

CELL_SIZE = 40  # Hücre boyutu (px)
VISITED_COLOR = "lightblue"
PATH_COLOR = "yellow"
START_COLOR = "green"
GOAL_COLOR = "red"
WALL_COLOR = "black"
EMPTY_COLOR = "white"

class MazeGUI:
    def __init__(self, master, rows=10, cols=10, wall_prob=0.25):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.wall_prob = wall_prob

        self.master.title("Labirent Arama Algoritmaları")
        self.canvas = tk.Canvas(master, width=cols*CELL_SIZE, height=rows*CELL_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4)

        # Yeni labirent butonu
        tk.Button(master, text="Yeni Labirent", command=self.new_maze).grid(row=1, column=0)

        # Algoritma butonları
        tk.Button(master, text="BFS Animasyonu", command=lambda: self.run_algorithm("BFS")).grid(row=1, column=1)
        tk.Button(master, text="DFS Animasyonu", command=lambda: self.run_algorithm("DFS")).grid(row=1, column=2)
        tk.Button(master, text="A* Animasyonu", command=lambda: self.run_algorithm("A*")).grid(row=1, column=3)

        # Performans tablosu
        self.tree = ttk.Treeview(master, columns=("Adım", "Genişletilen", "Süre", "Yol Kalitesi"), show="headings")
        self.tree.heading("Adım", text="Adım")
        self.tree.heading("Genişletilen", text="Genişletilen")
        self.tree.heading("Süre", text="Süre (sn)")
        self.tree.heading("Yol Kalitesi", text="Yol Kalitesi (%)")
        self.tree.grid(row=2, column=0, columnspan=4)

        self.new_maze()

    def new_maze(self):
        self.maze, self.start, self.goal = generate_maze(self.rows, self.cols, self.wall_prob)
        self.draw_maze()
        self.tree.delete(*self.tree.get_children())  # Tabloyu temizle

    def draw_maze(self, path=None, visited_cells=None):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = EMPTY_COLOR
                if (i,j) == self.start:
                    color = START_COLOR
                elif (i,j) == self.goal:
                    color = GOAL_COLOR
                elif self.maze[i][j] == 1:
                    color = WALL_COLOR
                if visited_cells and (i,j) in visited_cells:
                    color = VISITED_COLOR
                if path and (i,j) in path:
                    color = PATH_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def animate(self, steps):
        def step(i=0):
            if i < len(steps):
                position, path = steps[i]
                self.draw_maze(path=path, visited_cells=[pos for pos,_ in steps[:i+1]])
                self.master.after(100, step, i+1)
        step()


    def run_algorithm(self, algorithm_name):
        algorithms = {"BFS": bfs, "DFS": dfs, "A*": astar}
        func = algorithms[algorithm_name]

        start_time = time.time()
        path, expanded, steps = func(self.start, self.goal, self.maze)
        end_time = time.time()
        duration = round(end_time - start_time, 4)

        shortest_path, _, _ = bfs(self.start, self.goal, self.maze)
        shortest_len = len(shortest_path)-1 if shortest_path else None
        steps_count = len(path)-1 if path else 0
        quality = calculate_path_quality(shortest_len, steps_count) if shortest_len else 0

        if steps:
            self.animate(steps)

        self.tree.insert("", "end", values=(steps_count, expanded, duration, quality))


if __name__ == "__main__":
    root = tk.Tk()
    gui = MazeGUI(root)
    root.mainloop()
