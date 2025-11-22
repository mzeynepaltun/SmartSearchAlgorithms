import heapq  # A* algoritması için öncelikli kuyruk (priority queue) desteği
from utils.neighbors import get_neighbors

# ---------------------------------------
# A* (A-STAR) ARAMA ALGORİTMASI
# ---------------------------------------
def manhattan(a, b): # Heuristic Function, tahmini maliyet fonksiyonu
    """
    Manhattan mesafesi: iki hücre arasındaki 'şehiriçi' uzaklık.
    a, b: (row, col) koordinatları
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def astar(start, goal, maze):
    """
    Labirentte en kısa yolu bulmak için A* algoritmasını uygular.
    
    A* = g(n) + h(n)
    g(n) = başlangıçtan n hücresine kadar olan maliyet
    h(n) = n hücresinden hedefe olan tahmini maliyet (heuristic)
    """
    
    open_set = []  # Öncelikli kuyruk: (f, g, position, path)
    heapq.heappush(open_set, (0 + manhattan(start, goal), 0, start, [start])) # Başlangıç düğümü
    visited = set()  # Ziyaret edilen hücreler
    expanded = 0      # Genişletilen hücre sayısı

    while open_set:
        f, g, position, path = heapq.heappop(open_set)  # f değeri en düşük olanı al
        expanded += 1

        if position == goal:          # Hedefe ulaşıldı mı?
            return path, expanded

        if position in visited:       # Zaten ziyaret edilmişse atla
            continue
        visited.add(position)         # Ziyaret edilenlere ekle

        # Komşuları kontrol et
        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:
                new_g = g + 1  # Mevcut maliyeti 1 artır (her adım maliyeti 1)
                new_f = new_g + manhattan(neighbor, goal)  # Toplam f = g + h
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))
    return [], expanded
