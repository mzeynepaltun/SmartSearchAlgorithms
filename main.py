import tkinter as tk
from tkinter import ttk
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from utils.maze import generate_maze
import time

# ------------------------------------------------------------
# Sabitler ve renk tanımları
# ------------------------------------------------------------
CELL_SIZE = 40  # Her hücrenin piksel boyutu
VISITED_COLOR = "lightblue"  # Ziyaret edilmiş hücreler
PATH_COLOR = "yellow"        # Bulunan yol
START_COLOR = "green"        # Başlangıç hücresi
GOAL_COLOR = "red"           # Hedef hücresi
WALL_COLOR = "black"         # Duvar hücresi
EMPTY_COLOR = "white"        # Boş yol

# ------------------------------------------------------------
# Ana GUI sınıfı
# ------------------------------------------------------------
class MazeGUI:
    def __init__(self, master, rows=10, cols=10, wall_prob=0.25):
        """
        GUI'yi başlatır, labirent boyutu, hücre olasılığı ve
        arayüz elemanlarını oluşturur.
        """
        self.master = master
        self.rows = rows
        self.cols = cols
        self.wall_prob = wall_prob

        self.master.title("Labirent Arama Algoritmaları")

        # --- Durum Etiketi ---
        # Algoritma çalışırken veya çözüm yoksa kullanıcıya bilgi verir
        self.status_label = tk.Label(master, text="Hazır", font=("Arial", 14, "bold"), fg="blue")
        self.status_label.grid(row=0, column=0, columnspan=4, pady=5)

        # Labirent canvas'ı: labirenti görselleştirir
        self.canvas = tk.Canvas(master, width=cols*CELL_SIZE, height=rows*CELL_SIZE)
        self.canvas.grid(row=1, column=0, columnspan=4)

        # Butonlar
        tk.Button(master, text="Yeni Labirent", command=self.new_maze).grid(row=2, column=0)
        tk.Button(master, text="BFS Animasyonu", command=lambda: self.run_algorithm("BFS")).grid(row=2, column=1)
        tk.Button(master, text="DFS Animasyonu", command=lambda: self.run_algorithm("DFS")).grid(row=2, column=2)
        tk.Button(master, text="A* Animasyonu", command=lambda: self.run_algorithm("A*")).grid(row=2, column=3)

        # Performans tablosu (Treeview)
        self.tree = ttk.Treeview(master, columns=("Adım Sayısı", "Genişletilen Düğüm Sayısı", "Süre", "Yol Kalitesi"), show="headings")
        self.tree.heading("Adım Sayısı", text="Adım Sayısı")
        self.tree.heading("Genişletilen Düğüm Sayısı", text="Genişletilen Düğüm Sayısı")
        self.tree.heading("Süre", text="Süre (sn)")
        self.tree.heading("Yol Kalitesi", text="Yol Kalitesi (%)")
        self.tree.grid(row=3, column=0, columnspan=4)

        # Başlangıçta bir labirent oluştur
        self.new_maze()

    # ------------------------------------------------------------
    # Yeni labirent oluşturma
    # ------------------------------------------------------------
    def new_maze(self):
        """
        generate_maze fonksiyonunu çağırarak yeni labirent oluşturur,
        canvas'ı çizdirir ve performans tablosunu temizler.
        """
        self.maze, self.start, self.goal = generate_maze(self.rows, self.cols, self.wall_prob)
        self.status_label.config(text="Yeni Labirent Oluşturuldu", fg="black")
        self.draw_maze()
        self.tree.delete(*self.tree.get_children())

    # ------------------------------------------------------------
    # Labirenti çizme fonksiyonu
    # ------------------------------------------------------------
    def draw_maze(self, path=None, visited_cells=None):
        """
        Canvas üzerinde labirenti çizer. 
        Parametreler:
        - path: Bulunan çözüm yolu
        - visited_cells: Algoritma tarafından ziyaret edilen hücreler
        """
        self.canvas.delete("all")  # Önceki çizimleri sil
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = EMPTY_COLOR

                # Başlangıç ve hedef hücresi
                if (i,j) == self.start:
                    color = START_COLOR
                elif (i,j) == self.goal:
                    color = GOAL_COLOR
                # Duvar hücresi
                elif self.maze[i][j] == 1:
                    color = WALL_COLOR
                # Ziyaret edilmiş hücreler
                if visited_cells and (i,j) in visited_cells:
                    color = VISITED_COLOR
                # Bulunan yol
                if path and (i,j) in path:
                    color = PATH_COLOR

                # Hücreyi canvas üzerinde oluştur
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ------------------------------------------------------------
    # Animasyon fonksiyonu
    # ------------------------------------------------------------
    def animate(self, steps, algorithm_name, success):
        """
        Algoritmanın adım adım animasyonunu gösterir.
        steps: [(pozisyon, path), ...] formatında adımlar
        algorithm_name: Animasyon başlığı ve durum etiketi için
        success: True ise çözüm bulundu, False ise çözüm yok
        """
        def step(i=0):
            if i < len(steps):
                position, path = steps[i]

                # Status label güncelle: kaç düğüm gezildi
                self.status_label.config(
                    text=f"{algorithm_name} / Genişletilen Düğüm Sayısı: {i + 1}", 
                    fg="blue"
                )

                # Canvas'ı yeniden çiz
                self.draw_maze(path=path, visited_cells=[pos for pos,_ in steps[:i+1]])

                # 100ms sonra bir sonraki adımı çalıştır
                self.master.after(100, step, i+1)
            else:
                # Animasyon bittiğinde durumu göster
                if success:
                    self.status_label.config(
                        text=f"{algorithm_name} Tamamlandı / Toplam: {len(steps)}", 
                        fg="green"
                    )
                else:
                    self.status_label.config(text=f"{algorithm_name}: Çözüm Bulunamadı!", fg="red")
        step()

    # ------------------------------------------------------------
    # Algoritmayı çalıştırma ve animasyonu başlatma
    # ------------------------------------------------------------
    def run_algorithm(self, algorithm_name):
        """
        Seçilen algoritmayı çalıştırır, animasyonu başlatır ve performans tablosunu günceller.
        """
        algorithms = {"BFS": bfs, "DFS": dfs, "A*": astar}
        func = algorithms[algorithm_name]

        # Durum etiketini hazırlık için güncelle
        self.status_label.config(text=f"{algorithm_name} hazırlanıyor...", fg="orange")
        self.master.update()  # Label'ı hemen güncelle

        # Yol kalitesi hesaplama fonksiyonu
        def calculate_path_quality(shortest_len, current_len):
            """
            En kısa yolun uzunluğuna göre mevcut yolun kalitesini yüzdelik olarak döner
            """
            if current_len is None or current_len == 0:
                return 0
            return round((shortest_len / current_len) * 100, 2)

        # Algoritmayı çalıştır ve süreyi ölç
        start_time = time.time()
        path, expanded, steps = func(self.start, self.goal, self.maze)
        end_time = time.time()
        duration = round(end_time - start_time, 4)

        # Çözüm olup olmadığını belirle
        success = (path is not None)

        # Eğer algoritma adım üretemediyse direkt çözüm yok uyarısı
        if not steps and not success:
            self.status_label.config(text="Çözüm Bulunamadı!", fg="red")

        # En kısa yol referansı (BFS ile)
        shortest_path, _, _ = bfs(self.start, self.goal, self.maze)
        shortest_len = len(shortest_path)-1 if shortest_path else None
        steps_count = len(path)-1 if path else 0
        quality = calculate_path_quality(shortest_len, steps_count) if shortest_len else 0

        # Adım adım animasyon varsa çalıştır
        if steps:
            self.animate(steps, algorithm_name, success)

        # Performans tablosuna ekle
        self.tree.insert("", "end", values=(steps_count, expanded, duration, quality))

# ------------------------------------------------------------
# Program doğrudan çalıştırıldığında GUI başlatılır
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = MazeGUI(root)
    root.mainloop()
