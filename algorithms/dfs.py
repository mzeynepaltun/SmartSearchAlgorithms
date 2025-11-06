from utils.neighbors import get_neighbors

# ---------------------------------------
# DFS (Depth-First Search) ALGORİTMASI
# ---------------------------------------
def dfs(start, goal, maze):
    """
    Labirentte bir yol bulmak için DFS kullanır.
    DFS, derinlemesine arama yapar (önce bir yolu sonuna kadar takip eder).
    """
    
    stack = [(start, [start])]  # LIFO stack: (mevcut pozisyon, o ana kadar olan yol)
    visited = {start}           # Ziyaret edilen hücreler
    expanded = 0                # Genişletilen hücre sayısı
    
    while stack:
        position, path = stack.pop()  # Stackin tepesinden çıkar (en son eklenen)
        expanded += 1
        
        if position == goal:          # Hedefe ulaşıldı mı?
            return path, expanded
        
        # Komşuları kontrol et
        for neighbor in get_neighbors(position, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))  # Stackin tepesine ekle
    return None, expanded
