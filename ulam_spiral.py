#!/usr/bin/env python3
"""
Generator Spirali Ulama
Generuje spiralę Ulama dla zadanej liczby n i wizualizuje ją z zaznaczonymi liczbami pierwszymi.
"""

import math
import sys
import time
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Set
import xml.etree.ElementTree as ET


def czy_pierwsza(n: int) -> bool:
    """Wysoce zoptymalizowane sprawdzanie pierwszości z faktoryzacją kołową."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Użyj faktoryzacji kołowej 6k±1 - sprawdzaj tylko liczby postaci 6k±1
    i = 5
    sqrt_n = int(math.sqrt(n)) + 1
    while i < sqrt_n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# Nazwa pliku cache dla liczb pierwszych
PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"


def wczytaj_cache_pierwszych() -> Tuple[Set[int], int]:
    """Wczytaj cache liczb pierwszych z pliku. Zwraca (zbiór_pierwszych, maksymalna_sprawdzona_liczba)."""
    if not os.path.exists(PLIK_CACHE_PIERWSZYCH):
        return set(), 1

    try:
        with open(PLIK_CACHE_PIERWSZYCH, 'rb') as f:
            dane = pickle.load(f)
            pierwsze = dane.get('pierwsze', set())
            max_sprawdzone = dane.get('max_sprawdzone', 1)
            return pierwsze, max_sprawdzone
    except (FileNotFoundError, pickle.UnpicklingError, KeyError):
        return set(), 1


def zapisz_cache_pierwszych(pierwsze: Set[int], max_sprawdzone: int):
    """Zapisz cache liczb pierwszych do pliku."""
    try:
        dane = {
            'pierwsze': pierwsze,
            'max_sprawdzone': max_sprawdzone
        }
        with open(PLIK_CACHE_PIERWSZYCH, 'wb') as f:
            pickle.dump(dane, f)
    except Exception as e:
        print(f"  Ostrzeżenie: Nie można zapisać cache liczb pierwszych: {e}")


def wyswietl_postep(aktualny, calkowity, prefix="Postęp", dlugosc=50):
    """Wyświetla pasek postępu który pozostaje w miejscu."""
    procent = (aktualny / calkowity) * 100
    wypelniona_dlugosc = int(dlugosc * aktualny // calkowity)
    pasek = '█' * wypelniona_dlugosc + '-' * (dlugosc - wypelniona_dlugosc)
    sys.stdout.write(f'\r{prefix}: |{pasek}| {procent:.1f}% ({aktualny:,}/{calkowity:,})')
    sys.stdout.flush()
    if aktualny == calkowity:
        sys.stdout.write('\n')  # Nowa linia po zakończeniu
        sys.stdout.flush()


def sito_eratostenesa_z_cache(limit: int) -> Set[int]:
    """Zoptymalizowane Sito Eratostenesa z systemem cache."""
    if limit < 2:
        return set()

    print(f"    Krok 1/4: Wczytywanie cache liczb pierwszych...")
    pierwsze_cache, max_sprawdzone = wczytaj_cache_pierwszych()

    if max_sprawdzone >= limit:
        # Cache zawiera wszystkie potrzebne liczby pierwsze
        pierwsze_wynik = {p for p in pierwsze_cache if p <= limit}
        print(
            f"    Cache zawiera wszystkie liczby do {limit:,} - znaleziono {len(pierwsze_wynik):,} liczb pierwszych")
        return pierwsze_wynik

    print(f"    Cache zawiera liczby do {max_sprawdzone:,}, rozszerzanie do {limit:,}...")

    print(f"    Krok 2/4: Inicjalizacja sita dla zakresu {max_sprawdzone + 1:,} - {limit:,}...")

    # Rozpocznij od następnej liczby niesprawdzonej
    start_range = max_sprawdzone + 1

    # Użyj numpy boolean array dla lepszej wydajności
    sito = np.ones(limit + 1, dtype=bool)
    sito[0] = sito[1] = False

    # Oznacz liczby z cache jako pierwsze
    for p in pierwsze_cache:
        if p <= limit:
            sito[p] = True

    print(f"    Krok 3/4: Uruchamianie algorytmu sita dla nowego zakresu...")
    sqrt_limit = int(math.sqrt(limit))

    # Optymalizuj poprzez osobne obsłużenie 2 a potem tylko liczby nieparzyste
    if limit >= 2:
        # Oznacz wszystkie liczby parzyste jako złożone (oprócz 2)
        sito[4::2] = False

    # Użyj liczb pierwszych z cache do przesiewania nowego zakresu
    for p in pierwsze_cache:
        if p * p > limit:
            break
        # Znajdź pierwszy wielokrotność p w nowym zakresie
        start_multiple = ((start_range + p - 1) // p) * p
        if start_multiple < p * p:
            start_multiple = p * p

        # Oznacz wielokrotności
        for multiple in range(start_multiple, limit + 1, p):
            if multiple != p:  # Nie oznaczaj samej liczby pierwszej
                sito[multiple] = False

    # Sprawdzaj nowe liczby pierwsze w zakresie który nie był jeszcze sprawdzony
    for i in range(max(3, start_range), sqrt_limit + 1, 2):
        if i % max(1, sqrt_limit // 50) == 0 or i == sqrt_limit:
            wyswietl_postep(i, sqrt_limit, "    Przesiewanie")
        if sito[i]:
            # Zacznij od i*i i krok 2*i aby oznaczyć tylko nieparzyste wielokrotności
            start_multiple = max(i * i, start_range)
            for multiple in range(start_multiple, limit + 1, 2 * i):
                sito[multiple] = False

    # Upewnij się, że pasek postępu jest zakończony
    if sqrt_limit > 0:
        wyswietl_postep(sqrt_limit, sqrt_limit, "    Przesiewanie")

    print(f"    Krok 4/4: Zbieranie i zapisywanie wyników...")
    # Użyj numpy where do szybkiego zbierania
    wszystkie_pierwsze = set(np.where(sito)[0])

    # Zapisz rozszerzony cache
    zapisz_cache_pierwszych(wszystkie_pierwsze, limit)

    print(f"    Sito zakończone - znaleziono {len(wszystkie_pierwsze):,} liczb pierwszych")
    print(f"    Cache zaktualizowany do zakresu {limit:,}")

    return wszystkie_pierwsze


def sprawdzanie_pierwszosci_z_cache(n: int) -> Set[int]:
    """Sprawdzanie pierwszości z użyciem cache dla dużych zakresów."""
    print(f"  Używanie zoptymalizowanego sprawdzania indywidualnego z cache dla {n:,} liczb...")

    # Wczytaj cache
    pierwsze_cache, max_sprawdzone = wczytaj_cache_pierwszych()
    pierwsze = set(pierwsze_cache)

    if max_sprawdzone >= n:
        # Cache zawiera wszystkie potrzebne liczby
        wynik = {p for p in pierwsze if p <= n}
        print(f"  Cache zawiera wszystkie liczby do {n:,} - użyto {len(wynik):,} liczb pierwszych")
        return wynik

    print(f"  Cache zawiera liczby do {max_sprawdzone:,}, sprawdzanie do {n:,}...")

    # Dodaj małe liczby pierwsze ręcznie jeśli nie są w cache
    if 2 <= n and 2 not in pierwsze:
        pierwsze.add(2)
    if 3 <= n and 3 not in pierwsze:
        pierwsze.add(3)

    # Sprawdź tylko nowe liczby nieparzyste
    start_range = max(max_sprawdzone + 1, 5)
    if start_range % 2 == 0:  # Upewnij się że zaczynamy od liczby nieparzystej
        start_range += 1

    for i in range(start_range, n + 1, 2):
        if i % max(1, n // 100) == 0 or i == n or (i == n - 1 and n % 2 == 0):
            wyswietl_postep(i, n, "  Sprawdzanie pierwszości")
        if czy_pierwsza(i):
            pierwsze.add(i)

    # Upewnij się, że pasek postępu jest zakończony
    wyswietl_postep(n, n, "  Sprawdzanie pierwszości")

    # Zapisz rozszerzony cache
    zapisz_cache_pierwszych(pierwsze, n)
    print(f"  Cache zaktualizowany do zakresu {n:,}")

    return pierwsze


def generuj_wspolrzedne_spirali(n: int) -> List[Tuple[int, int]]:
    """Generuj współrzędne dla spirali Ulama od 1 do n."""
    if n <= 0:
        return []

    wspolrzedne = [(0, 0)]  # Zacznij od środka z liczbą 1

    if n == 1:
        return wspolrzedne

    print(f"    Generowanie współrzędnych spirali dla {n:,} liczb...")
    x, y = 0, 0
    dx, dy = 1, 0  # Zacznij ruch w prawo
    kroki = 1

    for num in range(2, n + 1):
        if num % max(1, n // 100) == 0 or num == n:  # Aktualizuj co 1% i na końcu
            wyswietl_postep(num, n, "    Generowanie spirali")

        x += dx
        y += dy
        wspolrzedne.append((x, y))

        kroki -= 1

        if kroki == 0:
            # Zmień kierunek: prawo -> góra -> lewo -> dół -> prawo
            dx, dy = -dy, dx

            # Zwiększ liczbę kroków po ruchu w prawo lub lewo
            if dx != 0:
                kroki = abs(x) * 2 if x > 0 else abs(x) * 2 + 1
            else:
                kroki = abs(y) * 2 if y > 0 else abs(y) * 2 + 1

    print(f"    Współrzędne spirali wygenerowane pomyślnie")
    return wspolrzedne


def utworz_spirale_ulama(
        n: int, uzyj_sito: bool = True) -> Tuple[np.ndarray, List[Tuple[int, int]], Set[int]]:
    """Utwórz strukturę danych spirali Ulama."""
    print(f"\n=== GENEROWANIE SPIRALI ULAMA DLA n={n:,} ===")
    czas_start = time.time()

    # Generuj liczby pierwsze
    print(f"\n[1/4] GENEROWANIE LICZB PIERWSZYCH")
    if uzyj_sito and n <= 10**7:  # Użyj sita dla rozsądnych rozmiarów
        print(f"  Używanie Sita Eratostenesa z cache do generowania liczb pierwszych...")
        pierwsze = sito_eratostenesa_z_cache(n)
    else:
        pierwsze = sprawdzanie_pierwszosci_z_cache(n)

    print(f"  ✓ Znaleziono {len(pierwsze):,} liczb pierwszych")

    # Generuj współrzędne spirali
    print(f"\n[2/4] GENEROWANIE WSPÓŁRZĘDNYCH SPIRALI")
    wspolrzedne = generuj_wspolrzedne_spirali(n)

    # Oblicz rozmiar siatki
    print(f"\n[3/4] PRZYGOTOWANIE SIATKI")
    print(f"  Obliczanie wymiarów siatki...")
    max_wsp = max(max(abs(x), abs(y)) for x, y in wspolrzedne)
    rozmiar_siatki = 2 * max_wsp + 1
    print(f"  Rozmiar siatki: {rozmiar_siatki}x{rozmiar_siatki} ({rozmiar_siatki**2:,} komórek)")

    # Utwórz siatkę
    print(f"  Inicjalizacja tablicy siatki...")
    siatka = np.zeros((rozmiar_siatki, rozmiar_siatki), dtype=int)
    przesuniecie = max_wsp  # Przesunięcie środka

    # Wypełnij siatkę liczbami
    print(f"  Wypełnianie siatki liczbami...")
    for i, (x, y) in enumerate(wspolrzedne, 1):
        if i % max(1, len(wspolrzedne) // 50) == 0 or i == len(wspolrzedne):
            wyswietl_postep(i, len(wspolrzedne), "  Wypełnianie siatki")
        siatka[przesuniecie - y, przesuniecie + x] = i  # Uwaga: y jest odwrócone do wyświetlenia

    czas_uplyniety = time.time() - czas_start
    print(f"\n[4/4] GENEROWANIE SPIRALI ZAKOŃCZONE")
    print(f"  ✓ Całkowity czas: {czas_uplyniety:.2f} sekund")

    return siatka, wspolrzedne, pierwsze


def generuj_svg_spirali_ulama(wspolrzedne: List[Tuple[int, int]], pierwsze: Set[int],
                              nazwa_pliku: str = "spirala_ulama.svg", rozmiar_punktu: float = 1.0,
                              margines: int = 20) -> str:
    """Generuj grafiku wektorową SVG spirali Ulama z całym cache."""
    print("\n=== GENEROWANIE GRAFIKI WEKTOROWEJ SVG ===")

    if not wspolrzedne:
        print("  Błąd: Brak współrzędnych do wygenerowania SVG")
        return ""

    print(f"  Przygotowywanie danych dla {len(wspolrzedne):,} punktów...")

    # Znajdź zakres współrzędnych
    min_x = min(x for x, y in wspolrzedne)
    max_x = max(x for x, y in wspolrzedne)
    min_y = min(y for x, y in wspolrzedne)
    max_y = max(y for x, y in wspolrzedne)

    # Oblicz rozmiar SVG
    szerokosc_danych = max_x - min_x
    wysokosc_danych = max_y - min_y
    szerokosc_svg = szerokosc_danych * rozmiar_punktu + 2 * margines
    wysokosc_svg = wysokosc_danych * rozmiar_punktu + 2 * margines

    print(f"  Zakres współrzędnych: X({min_x}, {max_x}), Y({min_y}, {max_y})")
    print(f"  Rozmiar SVG: {szerokosc_svg:.1f}x{wysokosc_svg:.1f}")
    print(
        f"  Liczby pierwsze w zakresie: {len([i for i in range(1, len(wspolrzedne) + 1) if i in pierwsze]):,}")

    # Utwórz element root SVG
    root = ET.Element("svg", {
        "width": f"{szerokosc_svg:.1f}",
        "height": f"{wysokosc_svg:.1f}",
        "viewBox": f"0 0 {szerokosc_svg:.1f} {wysokosc_svg:.1f}",
        "xmlns": "http://www.w3.org/2000/svg"
    })


    # Dodaj style
    style = ET.SubElement(root, "style")
    style.text = """
        .prime { fill: #333333; stroke: none; }
        .composite { fill: #cccccc; stroke: none; }
        .background { fill: white; }
    """

    # Dodaj tło
    ET.SubElement(root, "rect", {
        "class": "background",
        "width": f"{szerokosc_svg:.1f}",
        "height": f"{wysokosc_svg:.1f}"
    })

    # Dodaj grupę dla punktów
    grupa_punktow = ET.SubElement(root, "g", {"id": "points"})

    # Generuj punkty
    print("  Generowanie punktów SVG...")
    licznik_pierwszych = 0

    for i, (x, y) in enumerate(wspolrzedne, 1):
        if i % max(1, len(wspolrzedne) // 50) == 0 or i == len(wspolrzedne):
            wyswietl_postep(i, len(wspolrzedne), "  Generowanie punktów")

        # Przekształć współrzędne do układu SVG
        svg_x = (x - min_x) * rozmiar_punktu + margines
        svg_y = (max_y - y) * rozmiar_punktu + margines  # Odwróć Y dla SVG

        # Określ czy liczba jest pierwsza
        czy_pierwsza_liczba = i in pierwsze
        if czy_pierwsza_liczba:
            licznik_pierwszych += 1

        # Dodaj punkt (kwadrat dla liczb pierwszych, koło dla złożonych)
        klasa = "prime" if czy_pierwsza_liczba else "composite"
        if czy_pierwsza_liczba:
            # Kwadrat dla liczb pierwszych
            rozmiar_kwadratu = rozmiar_punktu * 1.6
            ET.SubElement(grupa_punktow, "rect", {
                "x": f"{svg_x - rozmiar_kwadratu/2:.2f}",
                "y": f"{svg_y - rozmiar_kwadratu/2:.2f}",
                "width": f"{rozmiar_kwadratu:.2f}",
                "height": f"{rozmiar_kwadratu:.2f}",
                "class": klasa
            })
        else:
            # Koło dla liczb złożonych
            ET.SubElement(grupa_punktow, "circle", {
                "cx": f"{svg_x:.2f}",
                "cy": f"{svg_y:.2f}",
                "r": f"{rozmiar_punktu * 0.8:.2f}",
                "class": klasa
            })



    # Zapisz SVG
    print(f"  Zapisywanie SVG do pliku: {nazwa_pliku}")
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(nazwa_pliku, encoding='utf-8', xml_declaration=True)

    print(f"  ✓ Grafika wektorowa SVG zapisana: {nazwa_pliku}")
    print(f"  ✓ Rozmiar pliku: {os.path.getsize(nazwa_pliku) / 1024 / 1024:.2f} MB")
    print(f"  ✓ Zawiera {len(wspolrzedne):,} punktów ({licznik_pierwszych:,} pierwszych)")

    return nazwa_pliku


def wizualizuj_spirale_ulama(siatka: np.ndarray, pierwsze: Set[int], tytul: str = "Spirala Ulama"):
    """Wizualizuj spiralę Ulama z zaznaczonymi liczbami pierwszymi."""
    print("\n=== TWORZENIE WIZUALIZACJI ===")

    # Utwórz mapę kolorów: 0 dla nie-pierwszych, 1 dla pierwszych
    print("  Przygotowywanie siatki liczb pierwszych...")
    siatka_pierwszych = np.zeros_like(siatka, dtype=float)

    calkowite_komorki = siatka.shape[0] * siatka.shape[1]
    przetworzone = 0

    for i in range(siatka.shape[0]):
        for j in range(siatka.shape[1]):
            przetworzone += 1
            if przetworzone % max(1, calkowite_komorki //
                                  20) == 0 or przetworzone == calkowite_komorki:
                wyswietl_postep(przetworzone, calkowite_komorki, "  Mapowanie pierwszych")

            liczba = siatka[i, j]
            if liczba > 0 and liczba in pierwsze:
                siatka_pierwszych[i, j] = 1

    # Utwórz pojedynczy wykres dla liczb pierwszych
    print("  Tworzenie wizualizacji...")
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))

    # Utwórz siatkę tylko z liczbami pierwszymi (jednakowe wartości dla równomiernej widoczności)
    wyswietlenie_pierwszych = np.where(siatka_pierwszych > 0, 1, 0)

    # Użyj czarnego tła i czerwonych punktów dla liczb pierwszych
    ax.set_facecolor('black')
    im = ax.imshow(wyswietlenie_pierwszych, cmap='Reds', interpolation='nearest', vmin=0, vmax=1)
    ax.set_title(f'{tytul} - Liczby Pierwsze', fontsize=16, color='white')
    ax.set_xlabel('X', fontsize=14, color='white')
    ax.set_ylabel('Y', fontsize=14, color='white')

    # Dostosuj kolorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Liczby złożone', 'Liczby pierwsze'])
    cbar.ax.tick_params(colors='white')

    plt.tight_layout()
    print("  ✓ Wizualizacja zakończona")
    return fig


def main():
    """Główna funkcja do uruchomienia generatora spirali Ulama."""
    try:
        # Pobierz dane od użytkownika
        n = int(input("Wprowadź maksymalną liczbę dla spirali Ulama: "))

        if n <= 0:
            print("Proszę wprowadzić liczbę dodatnią.")
            return

        # Ostrzeż przed bardzo dużymi liczbami
        if n > 10**6:
            odpowiedz = input(
                f"Ostrzeżenie: n={n} jest dość duże. To może zająć czas i pamięć. Kontynuować? (t/n): ")
            if odpowiedz.lower() != 't':
                return

        # Generuj spiralę
        siatka, wspolrzedne, pierwsze = utworz_spirale_ulama(n)

        # Wyświetl statystyki
        print(f"\n=== STATYSTYKI ===")
        print(
            f"Rozmiar siatki: {siatka.shape[0]:,}x{siatka.shape[1]:,} ({siatka.shape[0]**2:,} komórek)")
        print(f"Całkowita liczba liczb: {n:,}")
        print(f"Liczby pierwsze: {len(pierwsze):,}")
        print(f"Gęstość liczb pierwszych: {len(pierwsze)/n*100:.2f}%")

        # Utwórz wizualizację PNG
        fig = wizualizuj_spirale_ulama(siatka, pierwsze, f"Spirala Ulama (n={n:,})")

        # Zapisz wykres PNG
        print(f"\n=== ZAPISYWANIE WYNIKÓW ===")
        nazwa_pliku_png = f"spirala_ulama_n{n}.png"
        print(f"  Zapisywanie wizualizacji PNG...")
        fig.savefig(nazwa_pliku_png, dpi=200, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Wizualizacja PNG zapisana jako: {nazwa_pliku_png}")

        # Generuj i zapisz wersję SVG z całym cache
        print(f"\n=== GENEROWANIE GRAFIKI WEKTOROWEJ SVG ===")
        nazwa_pliku_svg = f"spirala_ulama_n{n}.svg"

        # Określ rozmiar punktu na podstawie liczby punktów
        if n <= 1000:
            rozmiar_punktu = 3.0
        elif n <= 10000:
            rozmiar_punktu = 2.0
        elif n <= 100000:
            rozmiar_punktu = 1.5
        else:
            rozmiar_punktu = 1.0

        generuj_svg_spirali_ulama(wspolrzedne, pierwsze, nazwa_pliku_svg, rozmiar_punktu)

        # Pokaż wykres
        print(f"  Wyświetlanie wykresu PNG...")
        plt.show()
        print(f"\n=== GENEROWANIE SPIRALI ULAMA ZAKOŃCZONE ===")
        print(f"  ✓ Pliki wygenerowane:")
        print(f"    - PNG: {nazwa_pliku_png}")
        print(f"    - SVG: {nazwa_pliku_svg}")

    except ValueError:
        print("Proszę wprowadzić poprawną liczbę całkowitą.")
    except KeyboardInterrupt:
        print("\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
