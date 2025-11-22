from collections import deque
from utils.neighbors import get_neighbors

# ---------------------------------------
# BFS (Breadth-First Search) ALGORİTMASI
# ---------------------------------------
def bfs(start, goal, maze):
    """
    Labirentte en kısa yolu bulmak için BFS kullanır.
    
    start: başlangıç hücresi (tuple)
    goal: hedef hücresi (tuple)
    maze: 2D labirent listesi (0 = yol, 1 = duvar)
    return: path (bulunan yol listesi) ve expanded (genişletilen hücre sayısı)
    """
    
    queue = deque([(start, [start])])  # FIFO kuyruk: (mevcut pozisyon, o ana kadar olan yol)
    visited = {start}                  # Ziyaret edilen hücreleri tutar
    expanded = 0                       # Genişletilen hücre sayısı
    steps = []                         # Ziyaret edilen hücrelerin sırası
    
    while queue:
        position, path = queue.popleft()  # Kuyruğun başından çıkar (en eski eklenen)
        expanded += 1                     # Bu hücreyi genişlettik
        steps.append((position, list(path))) # Ziyaret edilen hücre sırasına ekle
        
        if position == goal:              # Hedefe ulaşıldı mı?
            return path, expanded, steps  # Yol ve toplam genişletilen hücre sayısını döndür
        
        # Mevcut hücrenin geçilebilir komşularını bul ve kuyrukta sıraya ekle
        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:   # Zaten ziyaret edilmemişse
                visited.add(neighbor)     # Ziyaret edilenlere ekle
                queue.append((neighbor, path + [neighbor]))  # Kuyruğa ekle, yol güncellenir
    return None, expanded, steps          # Eğer yol bulunamazsa None döndür
