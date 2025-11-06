import random  
# ---------------------------------------
# RASTGELE LABİRENT OLUŞTURAN FONKSİYON 
# ---------------------------------------

def generate_maze(rows=6, cols=6, wall_prob=0.25):
    """
    rows-cols: labirentin satır-sütun sayısı
    wall_prob: her bir hücrenin duvar olma olasılığı (0 ile 1 arasında)
    Bu fonksiyon ile 0'lar boş yol 1'ler duvar olmak üzere 
     bir labirent oluşturan 2D liste döndürülür.
    """
    maze = []
    
    for i in range(rows):
        row = []
        for j in range(cols):

            if random.random() < wall_prob: # Hücre duvar olma olasılığı kontrol ediliyor
                row.append(1)  # Hücre duvar olarak işaretleniyor
            else:
                row.append(0)  # Hücre boş yol olarak işaretleniyor
        maze.append(row)  # Oluşturulan satır labirente ekleniyor
    
    # Başlangıç ve hedef hücreleri her zaman boş yol olarak ayarlanıyor
    maze[0][0] = 0                 # başlangıç açık
    maze[rows - 1][cols - 1] = 0   # hedef açık
    
    # Oluşturulan labirent ve başlangıç-hedef koordinatları döndürülüyor
    return maze, (0, 0), (rows - 1, cols - 1)


# LABİRENTİ EKRANA YAZDIRAN FONKSİYON 
def print_maze(maze, start, goal, path=None):
    
    """
    maze: 2D liste (0 = boş, 1 = duvar)
    start: başlangıç hücresinin (x, y) koordinatları
    goal: hedef hücresinin (x, y) koordinatları
    path: eğer arama algoritması sonucu bulunmuş bir yol varsa, bu hücrelerin listesi
    """
    
    for i in range(len(maze)):  # Her satır için
        for j in range(len(maze[0])):  # Her sütun için
            if (i, j) == start:
                print("S", end=" ")  # Başlangıç noktası → S harfi
            elif (i, j) == goal:
                print("G", end=" ")  # Hedef noktası → G harfi
            elif path and (i, j) in path:
                print("X", end=" ")  # Eğer bir çözüm yolu verilmişse, o hücreleri X ile göster
            elif maze[i][j] == 1:
                print("#", end=" ")  # Duvar hücreleri → #
            else:
                print(".", end=" ")  # Boş yollar → .
        print()  # Her satır bitince alt satıra geçer
    print("-" * (2 * len(maze[0])))  # Labirent bittiğinde ayırıcı çizgi basar
