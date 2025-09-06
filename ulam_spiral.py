#!/usr/bin/env python3
"""
Generator Spirali Ulama
Generuje spiralę Ulama dla zadanej liczby n i wizualizuje ją z zaznaczonymi liczbami pierwszymi.
"""

import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Set


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


def sito_eratostenesa(limit: int) -> Set[int]:
    """Zoptymalizowane Sito Eratostenesa z podejściem segmentowym."""
    if limit < 2:
        return set()
    
    print(f"    Krok 1/3: Inicjalizacja zoptymalizowanego sita dla {limit:,} liczb...")
    
    # Użyj numpy boolean array dla lepszej wydajności
    sito = np.ones(limit + 1, dtype=bool)
    sito[0] = sito[1] = False
    
    print(f"    Krok 2/3: Uruchamianie zoptymalizowanego algorytmu sita...")
    sqrt_limit = int(math.sqrt(limit))
    
    # Optymalizuj poprzez osobne obsłużenie 2 a potem tylko liczby nieparzyste
    if limit >= 2:
        # Oznacz wszystkie liczby parzyste jako złożone (oprócz 2)
        sito[4::2] = False
    
    # Sprawdzaj tylko liczby nieparzyste zaczynając od 3
    for i in range(3, sqrt_limit + 1, 2):
        if i % 10000 == 0:
            wyswietl_postep(i, sqrt_limit, "    Przesiewanie")
        if sito[i]:
            # Zacznij od i*i i krok 2*i aby oznaczyć tylko nieparzyste wielokrotności
            sito[i*i::2*i] = False
    
    wyswietl_postep(sqrt_limit, sqrt_limit, "    Przesiewanie")
    
    print(f"    Krok 3/3: Zbieranie liczb pierwszych...")
    # Użyj numpy where do szybkiego zbierania
    pierwsze = set(np.where(sito)[0])
    
    print(f"    Sito zakończone - znaleziono {len(pierwsze):,} liczb pierwszych")
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
        if num % max(1, n // 100) == 0:  # Aktualizuj co 1% lub co liczbę dla małych n
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


def utworz_spirale_ulama(n: int, uzyj_sito: bool = True) -> Tuple[np.ndarray, List[Tuple[int, int]], Set[int]]:
    """Utwórz strukturę danych spirali Ulama."""
    print(f"\n=== GENEROWANIE SPIRALI ULAMA DLA n={n:,} ===")
    czas_start = time.time()
    
    # Generuj liczby pierwsze
    print(f"\n[1/4] GENEROWANIE LICZB PIERWSZYCH")
    if uzyj_sito and n <= 10**7:  # Użyj sita dla rozsądnych rozmiarów
        print(f"  Używanie Sita Eratostenesa do generowania liczb pierwszych...")
        pierwsze = sito_eratostenesa(n)
    else:
        print(f"  Używanie zoptymalizowanego sprawdzania indywidualnego dla {n:,} liczb...")
        pierwsze = set()
        # Dodaj małe liczby pierwsze ręcznie dla wydajności
        if n >= 2: pierwsze.add(2)
        if n >= 3: pierwsze.add(3)
        
        # Sprawdzaj tylko liczby nieparzyste zaczynając od 5
        for i in range(5, n + 1, 2):
            if i % max(1, n // 100) == 0:
                wyswietl_postep(i, n, "  Sprawdzanie pierwszości")
            if czy_pierwsza(i):
                pierwsze.add(i)
        
        wyswietl_postep(n, n, "  Sprawdzanie pierwszości")
    
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
        if i % max(1, len(wspolrzedne) // 50) == 0:
            wyswietl_postep(i, len(wspolrzedne), "  Wypełnianie siatki")
        siatka[przesuniecie - y, przesuniecie + x] = i  # Uwaga: y jest odwrócone do wyświetlenia
    
    czas_uplyniety = time.time() - czas_start
    print(f"\n[4/4] GENEROWANIE SPIRALI ZAKOŃCZONE")
    print(f"  ✓ Całkowity czas: {czas_uplyniety:.2f} sekund")
    
    return siatka, wspolrzedne, pierwsze


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
            if przetworzone % max(1, calkowite_komorki // 20) == 0:
                wyswietl_postep(przetworzone, calkowite_komorki, "  Mapowanie pierwszych")
            
            liczba = siatka[i, j]
            if liczba > 0 and liczba in pierwsze:
                siatka_pierwszych[i, j] = 1
    
    # Utwórz pojedynczy wykres dla liczb pierwszych
    print("  Tworzenie wizualizacji...")
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    # Pokaż tylko liczby pierwsze
    wyswietlenie_pierwszych = np.where(siatka_pierwszych > 0, siatka, 0)
    im = ax.imshow(wyswietlenie_pierwszych, cmap='Reds', interpolation='nearest')
    ax.set_title(f'{tytul} - Liczby Pierwsze', fontsize=16)
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    plt.colorbar(im, ax=ax, shrink=0.8)
    
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
            odpowiedz = input(f"Ostrzeżenie: n={n} jest dość duże. To może zająć czas i pamięć. Kontynuować? (t/n): ")
            if odpowiedz.lower() != 't':
                return
        
        # Generuj spiralę
        siatka, wspolrzedne, pierwsze = utworz_spirale_ulama(n)
        
        # Wyświetl statystyki
        print(f"\n=== STATYSTYKI ===")
        print(f"Rozmiar siatki: {siatka.shape[0]:,}x{siatka.shape[1]:,} ({siatka.shape[0]**2:,} komórek)")
        print(f"Całkowita liczba liczb: {n:,}")
        print(f"Liczby pierwsze: {len(pierwsze):,}")
        print(f"Gęstość liczb pierwszych: {len(pierwsze)/n*100:.2f}%")
        
        # Utwórz wizualizację
        fig = wizualizuj_spirale_ulama(siatka, pierwsze, f"Spirala Ulama (n={n:,})")
        
        # Zapisz wykres
        print(f"\n=== ZAPISYWANIE WYNIKÓW ===")
        nazwa_pliku = f"spirala_ulama_n{n}.png"
        print(f"  Zapisywanie wizualizacji...")
        fig.savefig(nazwa_pliku, dpi=200, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Wizualizacja zapisana jako: {nazwa_pliku}")
        
        # Pokaż wykres
        print(f"  Wyświetlanie wykresu...")
        plt.show()
        print(f"\n=== GENEROWANIE SPIRALI ULAMA ZAKOŃCZONE ===")
        
    except ValueError:
        print("Proszę wprowadzić poprawną liczbę całkowitą.")
    except KeyboardInterrupt:
        print("\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()