# ------------------------------------------------------------
# Bu modül, farklı arama algoritmalarının performansını
# karşılaştırmak için metrik hesaplama fonksiyonlarını içerir.
# ------------------------------------------------------------

import time

# ------------------------------------------------------------
# Yol kalitesi hesaplama fonksiyonu
# ------------------------------------------------------------
def calculate_path_quality(shortest_len, current_len):
    """
    En kısa yolun uzunluğuna göre mevcut yolun kalitesini hesaplar.
    Kalite yüzdelik (%) olarak döner.
    Örnek: En kısa yol 10 adım, mevcut yol 12 adım → kalite = 83.33%
    """
    if current_len is None or current_len == 0:
        return 0  # Eğer yol bulunamadıysa kalite 0
    return round((shortest_len / current_len) * 100, 2)


# ------------------------------------------------------------
# Algoritmaların performansını karşılaştıran ana fonksiyon
# ------------------------------------------------------------
def compare_algorithms(algorithms, maze, start, goal, shortest_path_func):
    """
    Verilen algoritmaları çalıştırarak performanslarını karşılaştırır.

    Parametreler:
    - algorithms: { "Algoritma Adı": fonksiyon } şeklinde sözlük
    - maze: Labirent matrisi (0: yol, 1: duvar)
    - start: Başlangıç koordinatı (örnek: (0, 0))
    - goal: Hedef koordinatı (örnek: (N-1, M-1))
    - shortest_path_func: Referans olarak kullanılacak en kısa yol algoritması (örneğin BFS)

    Döndürür:
    - results: Her algoritmanın adıyla ilişkilendirilmiş istatistiklerin bulunduğu sözlük
    """

    results = {}

    # Öncelikle BFS gibi bir algoritmayla en kısa yol referansı bulunur
    shortest_path, _ = shortest_path_func(start, goal, maze)
    shortest_len = len(shortest_path) - 1 if shortest_path else None

    # Her algoritma için test yapılır
    for name, func in algorithms.items():
        print(f"{name} algoritması çalıştırılıyor...\n")

        start_time = time.perf_counter()  # Zaman ölçümü başlat (Mikrosaniye hassasiyetinde)
        path, expanded = func(start, goal, maze)  # Algoritmayı çalıştır
        end_time = time.perf_counter()    # Zaman ölçümü bitir (Mikrosaniye hassasiyetinde)

        if path:
            steps = len(path) - 1                     # Toplam adım sayısı
            duration = round(end_time - start_time, 4) # Geçen süre (saniye)
            quality = calculate_path_quality(shortest_len, steps) if shortest_len else 0

            # Sonuçlar sözlüğüne ekle
            results[name] = {
                "adımlar": steps,
                "genişletilen_düğüm": expanded,
                "süre": duration,
                "yol_kalitesi(%)": quality
            }

            print(f"✅ {name} çözüme ulaştı!")
            print(f"Toplam adım sayısı: {steps}")
            print(f"Genişletilen düğüm sayısı: {expanded}")
            print(f"Geçen süre: {duration} saniye")
            print(f"Yol kalitesi: %{quality}\n")
        else:
            print(f"❌ {name} çözüm bulamadı.\n")

    return results


# ------------------------------------------------------------
# Sonuçları tablo halinde yazdıran yardımcı fonksiyon
# ------------------------------------------------------------
def print_comparison_table(results):
    """
    Karşılaştırma sonuçlarını düzenli bir tablo formatında yazdırır.
    """
    print("\n--- ALGORİTMA KARŞILAŞTIRMASI ---")
    print("{:<5} | {:<10} | {:<20} | {:<10} | {:<15}".format(
        "Alg.", "Adım", "Genişletilen Düğüm", "Süre (sn)", "Yol Kalitesi (%)"))
    print("-" * 75)

    for name, info in results.items():
        print("{:<5} | {:<10} | {:<20} | {:<10} | {:<15}".format(
            name,
            info["adımlar"],
            info["genişletilen_düğüm"],
            info["süre"],
            info["yol_kalitesi(%)"]
        ))
