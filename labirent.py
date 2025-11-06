import time
import random
import heapq
from collections import deque

# ---------------------------------------
# RASTGELE LABİRENT ÜRETİMİ
# ---------------------------------------
def generate_maze(rows=6, cols=6, wall_prob=0.25):
    maze = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < wall_prob:
                row.append(1)  # duvar
            else:
                row.append(0)  # yol
        maze.append(row)
    maze[0][0] = 0                # başlangıç açık
    maze[rows - 1][cols - 1] = 0  # hedef açık
    return maze, (0, 0), (rows - 1, cols - 1)

# ---------------------------------------
# LABİRENTİ EKRANA YAZDIR
# ---------------------------------------
def print_maze(maze, start, goal, path=None):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == goal:
                print("G", end=" ")
            elif path and (i, j) in path:
                print("*", end=" ")
            elif maze[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()
    print("-" * (2 * len(maze[0])))

# ---------------------------------------
# KOMŞULARI BUL
# ---------------------------------------
def get_neighbors(pos, maze):
    r, c = pos
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

# ---------------------------------------
# BFS
# ---------------------------------------
def bfs(start, goal, maze):
    queue = deque([(start, [start])])
    visited = {start}
    expanded = 0
    
    while queue:
        position, path = queue.popleft()
        expanded += 1
        
        if position == goal:
            return path, expanded
        
        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None, expanded

# ---------------------------------------
# DFS
# ---------------------------------------
def dfs(start, goal, maze):
    stack = [(start, [start])]
    visited = {start}
    expanded = 0
    
    while stack:
        position, path = stack.pop()
        expanded += 1
        
        if position == goal:
            return path, expanded
        
        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    return None, expanded

# ---------------------------------------
# A*
# ---------------------------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, maze):
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start, goal), 0, start, [start]))
    visited = set()
    expanded = 0

    while open_set:
        f, g, position, path = heapq.heappop(open_set)
        expanded += 1

        if position == goal:
            return path, expanded

        if position in visited:
            continue
        visited.add(position)

        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))
    return None, expanded

# ---------------------------------------
# ANA PROGRAM
# ---------------------------------------
rows, cols = 10, 10
maze, start, goal = generate_maze(rows, cols, wall_prob=0.25)

print("Rastgele Üretilen Labirent:")
print_maze(maze, start, goal)

algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "A*": astar
}

results = {}

for name, func in algorithms.items():
    print(f"{name} algoritması çalıştırılıyor...\n")
    start_time = time.time()
    path, expanded = func(start, goal, maze)
    end_time = time.time()
    
    if path:
        results[name] = {
            "adımlar": len(path) - 1,
            "süre": round(end_time - start_time, 4),
            "genişletilen_düğüm": expanded,
            "yol": path
        }
        
        print(f"✅ {name} çözüme ulaştı!")
        print("Toplam adım sayısı:", len(path) - 1)
        print("Genişletilen düğüm sayısı:", expanded)
        print("Geçen süre:", round(end_time - start_time, 4), "saniye\n")

        print("Adım adım çözüm:\n")
        for i in range(len(path)):
            print(f"Adım {i}: {path[i]}")
            print_maze(maze, start, goal, path[:i+1])
            time.sleep(0.3)
    else:
        print(f"❌ {name} çözüm bulamadı.\n")

# ---------------------------------------
# KARŞILAŞTIRMA TABLOSU
# ---------------------------------------
print("\n--- ALGORİTMA KARŞILAŞTIRMASI ---")
print("{:<5} | {:<10} | {:<20} | {:<10}".format("Alg.", "Adım", "Genişletilen Düğüm", "Süre (sn)"))
print("-" * 55)

for name, info in results.items():
    print("{:<5} | {:<10} | {:<20} | {:<10}".format(
        name, info["adımlar"], info["genişletilen_düğüm"], info["süre"]
    ))
