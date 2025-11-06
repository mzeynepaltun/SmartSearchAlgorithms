# ---------------------------------------
# KOMŞULARI BULAN FONKSİYON
# ---------------------------------------

def get_neighbors(position, maze):
    """
    Belirli bir hücrenin (position) etrafındaki geçilebilir 
     (yani duvar olmayan) komşu hücreleri döndürür.
    pos: (r, c) biçiminde bir tuple — mevcut hücrenin satır ve sütun indeksleri
    """
    
    row, column = position  # Mevcut hücrenin satır (r) ve sütun (c) indeksleri alınıyor
    
    # Olası dört hareket yönü: yukarı, aşağı, sol, sağ
    # Her biri (satır değişimi, sütun değişimi) olarak tanımlı
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    neighbors = [] # Geçerli komşuları saklamak için boş liste
    
    # Her bir yönde adım atılara olası komşular kontrol ediliyor
    for dr, dc in directions:
        nr, nc = row + dr, column + dc  # Yeni (komşu) hücrenin koordinatları hesaplanıyor
        
        # Aşağıdaki koşul üç şeyi kontrol eder:
        # nr, nc labirentin sınırları içinde mi?
        # maze[nr][nc] == 0 mı? (Yani orası bir duvar değil, geçilebilir yol mu?)
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
            neighbors.append((nr, nc))  # Şartlar sağlanıyorsa komşular listesine eklenir
    
    return neighbors  # Geçerli komşuların listesi döndürülür
