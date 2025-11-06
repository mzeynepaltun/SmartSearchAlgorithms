# main.py
# ------------------------------------------------------------
# Ana çalışma dosyası:
# 1. Labirent oluşturur.
# 2. BFS, DFS, A* gibi algoritmaları çağırır.
# 3. performance.py modülünü kullanarak sonuçları karşılaştırır.
# ------------------------------------------------------------
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from analysis.performance import compare_algorithms, print_comparison_table
from utils.maze import generate_maze, print_maze
import random

# ------------------------------------------------------------
# ANA PROGRAM BAŞLANGICI
# ------------------------------------------------------------
def main():
    # random.seed(42)  # Aynı labirent üzerinde değerlendirme için sabit değer  !!!!!!DENEME İÇİN BURADA!!!!!!!
    
    # Labirent boyutları ve duvar olasılığı belirlenir
    rows, cols = 10, 10
    wall_prob = 0.25  # %25 olasılıkla duvar olacak

    # Rastgele labirent oluştur
    maze, start, goal = generate_maze(rows, cols, wall_prob)
    
    # 🚨 HATA YÖNETİMİ: Başlangıç veya hedef kapalıysa
    if maze[start[0]][start[1]] == 1 or maze[goal[0]][goal[1]] == 1:
        raise ValueError("Başlangıç veya hedef nokta kapalı! Algoritmalar çalıştırılmayacak.")

    print("Rastgele Üretilen Labirent:")
    print_maze(maze, start, goal)

    # Kullanılacak algoritmalar sözlüğü
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": astar
    }

    # Algoritmaların performansını karşılaştır
    results = compare_algorithms(algorithms, maze, start, goal, bfs)

    # Sonuçları tablo halinde yazdır
    print_comparison_table(results)


# ------------------------------------------------------------
# Program doğrudan çalıştırıldığında main() fonksiyonunu çağırır
# ------------------------------------------------------------
main()
