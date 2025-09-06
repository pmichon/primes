#!/usr/bin/env python3
"""
Generator Cache Liczb Pierwszych
Generuje i zapisuje cache liczb pierwszych do pliku pierwsze_cache.pkl
dla przyspieszenia działania generatora spirali Ulama.
"""

import argparse
import math
import os
import pickle
import sys
import time
import psutil
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import Set, Tuple, List, Dict


# Nazwa pliku cache (taka sama jak w głównym skrypcie)
PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"


def wykryj_zasoby_systemu() -> Dict[str, int]:
    """Wykryj dostępne zasoby systemowe."""
    try:
        # Liczba rdzeni CPU
        cpu_rdzenie = cpu_count()
        cpu_fizyczne = psutil.cpu_count(logical=False) or cpu_rdzenie
        
        # Dostępna pamięć RAM w GB
        pamiec_gb = psutil.virtual_memory().available // (1024**3)
        
        return {
            'cpu_logiczne': cpu_rdzenie,
            'cpu_fizyczne': cpu_fizyczne,
            'pamiec_gb': pamiec_gb
        }
    except Exception:
        # Wartości domyślne w przypadku błędu
        return {
            'cpu_logiczne': cpu_count(),
            'cpu_fizyczne': cpu_count(),
            'pamiec_gb': 4
        }


def oblicz_optymalne_parametry(limit: int, zasoby: Dict[str, int] = None) -> Dict[str, int]:
    """Oblicz optymalne parametry dla generowania liczb pierwszych."""
    if zasoby is None:
        zasoby = wykryj_zasoby_systemu()
    
    cpu_logiczne = zasoby['cpu_logiczne']
    cpu_fizyczne = zasoby['cpu_fizyczne']
    pamiec_gb = zasoby['pamiec_gb']
    
    # Ogólne wytyczne optymalizacji
    if limit <= 1 * 10**6:
        # Małe liczby - standardowe sito, jeden proces
        return {
            'algorytm': 'standardowy',
            'procesy': 1,
            'rozmiar_segmentu': 0,
            'opis': 'Standardowe sito numpy'
        }
    
    elif limit <= 10 * 10**6:
        # Średnie liczby - segmentowane sito, jeden proces
        rozmiar_segmentu = min(limit // 10, 2 * 10**6)
        return {
            'algorytm': 'segmentowany',
            'procesy': 1,
            'rozmiar_segmentu': rozmiar_segmentu,
            'opis': f'Segmentowane sito (segmenty: {rozmiar_segmentu:,})'
        }
    
    elif limit <= 100 * 10**6:
        # Duże liczby - równoległe segmentowane sito
        # Optymalna liczba procesów: 2-4 dla CPU z hyperthreading, inaczej wszystkie rdzenie
        if cpu_logiczne > cpu_fizyczne:
            # Hyperthreading - użyj 75% rdzeni logicznych
            procesy = max(2, int(cpu_logiczne * 0.75))
        else:
            # Bez hyperthreading - użyj wszystkie rdzenie minus jeden
            procesy = max(2, cpu_fizyczne - 1)
        
        # Rozmiar segmentu zależny od pamięci
        if pamiec_gb >= 16:
            rozmiar_segmentu = 5 * 10**6
        elif pamiec_gb >= 8:
            rozmiar_segmentu = 2 * 10**6
        else:
            rozmiar_segmentu = 1 * 10**6
        
        return {
            'algorytm': 'rownolegle_segmentowany',
            'procesy': procesy,
            'rozmiar_segmentu': rozmiar_segmentu,
            'opis': f'Równoległe segmentowane sito ({procesy} procesów, segmenty: {rozmiar_segmentu:,})'
        }
    
    else:
        # Bardzo duże liczby - maksymalna optymalizacja
        # Więcej procesów dla bardzo dużych liczb
        if cpu_logiczne >= 16:
            procesy = min(cpu_logiczne, 12)  # Ogranicz do 12 procesów
        elif cpu_logiczne >= 8:
            procesy = cpu_logiczne - 1
        else:
            procesy = cpu_logiczne
        
        # Większe segmenty dla lepszej wydajności
        if pamiec_gb >= 32:
            rozmiar_segmentu = 20 * 10**6
        elif pamiec_gb >= 16:
            rozmiar_segmentu = 10 * 10**6
        elif pamiec_gb >= 8:
            rozmiar_segmentu = 5 * 10**6
        else:
            rozmiar_segmentu = 2 * 10**6
        
        return {
            'algorytm': 'rownolegle_segmentowany',
            'procesy': procesy,
            'rozmiar_segmentu': rozmiar_segmentu,
            'opis': f'Zoptymalizowane równoległe sito ({procesy} procesów, segmenty: {rozmiar_segmentu:,})'
        }


def wyswietl_konfiguracje_systemu(limit: int, parametry: Dict[str, int], zasoby: Dict[str, int]):
    """Wyświetl informacje o konfiguracji systemu i wybranych parametrach."""
    print(f"\n=== KONFIGURACJA SYSTEMU ===")
    print(f"CPU: {zasoby['cpu_fizyczne']} fizycznych, {zasoby['cpu_logiczne']} logicznych rdzeni")
    print(f"Dostępna pamięć: {zasoby['pamiec_gb']} GB")
    print(f"Limit generowania: {limit:,} liczb")
    
    print(f"\n=== WYBRANE PARAMETRY OPTYMALIZACJI ===")
    print(f"Algorytm: {parametry['opis']}")
    if parametry['procesy'] > 1:
        print(f"Procesy równoległe: {parametry['procesy']}")
    if parametry['rozmiar_segmentu'] > 0:
        print(f"Rozmiar segmentu: {parametry['rozmiar_segmentu']:,}")
        szacowana_liczba_segmentow = (limit + parametry['rozmiar_segmentu'] - 1) // parametry['rozmiar_segmentu']
        print(f"Szacowana liczba segmentów: {szacowana_liczba_segmentow:,}")


def wyswietl_postep(aktualny, calkowity, prefix="Postęp", dlugosc=50):
    """Wyświetla pasek postępu który pozostaje w miejscu."""
    procent = (aktualny / calkowity) * 100
    wypelniona_dlugosc = int(dlugosc * aktualny // calkowity)
    pasek = '█' * wypelniona_dlugosc + '-' * (dlugosc - wypelniona_dlugosc)
    sys.stdout.write(f'\r{prefix}: |{pasek}| {procent:.1f}% ({aktualny:,}/{calkowity:,})')
    sys.stdout.flush()
    if aktualny == calkowity:
        sys.stdout.write('\n')
        sys.stdout.flush()


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


def wczytaj_istniejacy_cache() -> Tuple[Set[int], int]:
    """Wczytaj istniejący cache liczb pierwszych z pliku."""
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


def zapisz_cache(pierwsze: Set[int], max_sprawdzone: int):
    """Zapisz cache liczb pierwszych do pliku."""
    dane = {
        'pierwsze': pierwsze,
        'max_sprawdzone': max_sprawdzone
    }
    with open(PLIK_CACHE_PIERWSZYCH, 'wb') as f:
        pickle.dump(dane, f)


def generuj_podstawowe_pierwsze(limit: int) -> np.ndarray:
    """Generuj podstawowe liczby pierwsze do sqrt(limit) używając prostego sita."""
    if limit < 4:
        return np.array([2, 3][:limit-1])
    
    sqrt_limit = int(math.sqrt(limit)) + 1
    sito = np.ones(sqrt_limit + 1, dtype=bool)
    sito[0] = sito[1] = False
    
    # Standardowe sito dla małych liczb z paskiem postępu
    sqrt_sqrt_limit = int(math.sqrt(sqrt_limit)) + 1
    for i in range(2, sqrt_sqrt_limit):
        if i % max(1, sqrt_sqrt_limit // 20) == 0 or i == sqrt_sqrt_limit - 1:
            wyswietl_postep(i, sqrt_sqrt_limit, "  Podstawowe")
        if sito[i]:
            sito[i*i::i] = False
    
    if sqrt_sqrt_limit > 2:
        wyswietl_postep(sqrt_sqrt_limit, sqrt_sqrt_limit, "  Podstawowe")
    
    return np.where(sito)[0]


def segmentowane_sito_z_kolem(start: int, koniec: int, pierwsze_podstawowe: np.ndarray) -> Set[int]:
    """Segmentowane sito z optymalizacją koła 2*3*5 = 30."""
    if start > koniec:
        return set()
    
    # Wzorzec koła 30: liczby nie podzielne przez 2, 3, 5
    # W każdym bloku 30 są to pozycje: 1, 7, 11, 13, 17, 19, 23, 29
    wzorzec_kola = np.array([1, 7, 11, 13, 17, 19, 23, 29])
    rozmiar_kola = 30
    
    # Oblicz rozmiar segmentu (tylko dla liczb w wzorcu koła)
    bloki_start = start // rozmiar_kola
    bloki_koniec = koniec // rozmiar_kola
    rozmiar_segmentu = (bloki_koniec - bloki_start + 1) * len(wzorzec_kola)
    
    # Inicjalizuj segment jako wszystkie liczby pierwsze
    segment = np.ones(rozmiar_segmentu, dtype=bool)
    
    # Mapowanie indeksów do rzeczywistych liczb
    def indeks_do_liczby(idx):
        blok = idx // len(wzorzec_kola)
        pos_w_bloku = idx % len(wzorzec_kola)
        return (bloki_start + blok) * rozmiar_kola + wzorzec_kola[pos_w_bloku]
    
    def liczba_do_indeksu(liczba):
        blok = liczba // rozmiar_kola - bloki_start
        reszta = liczba % rozmiar_kola
        try:
            pos_w_bloku = np.where(wzorzec_kola == reszta)[0][0]
            return blok * len(wzorzec_kola) + pos_w_bloku
        except IndexError:
            return -1  # Liczba nie jest w wzorcu koła
    
    # Przesiej segment używając podstawowych liczb pierwszych
    for p in pierwsze_podstawowe:
        if p <= 5:  # Pomin liczby użyte w kole
            continue
        if p * p > koniec:
            break
            
        # Znajdź pierwszą liczbę w segmencie podzielna przez p
        pierwsza_wielokrotnosc = ((start + p - 1) // p) * p
        if pierwsza_wielokrotnosc < p * p:
            pierwsza_wielokrotnosc = p * p
            
        # Oznacz wielokrotności p w segmencie
        for wielokrotnosc in range(pierwsza_wielokrotnosc, koniec + 1, p):
            idx = liczba_do_indeksu(wielokrotnosc)
            if 0 <= idx < len(segment):
                segment[idx] = False
    
    # Zbierz liczby pierwsze z segmentu
    pierwsze_w_segmencie = set()
    for i in range(len(segment)):
        if segment[i]:
            liczba = indeks_do_liczby(i)
            if start <= liczba <= koniec:
                pierwsze_w_segmencie.add(liczba)
    
    return pierwsze_w_segmencie


def segmentowane_sito_duze_liczby(limit: int, rozmiar_segmentu: int = 10**6) -> Set[int]:
    """Segmentowane sito zoptymalizowane dla bardzo dużych liczb."""
    if limit < 2:
        return set()
    
    print(f"Generowanie podstawowych liczb pierwszych...")
    pierwsze_podstawowe = generuj_podstawowe_pierwsze(limit)
    print(f"Wygenerowano {len(pierwsze_podstawowe):,} podstawowych liczb pierwszych")
    
    # Rozpocznij od małych liczb pierwszych
    wszystkie_pierwsze = set(pierwsze_podstawowe[pierwsze_podstawowe <= int(math.sqrt(limit)) + 100])
    
    # Dodaj małe liczby pierwsze które są poniżej pierwszego segmentu
    start_segmentow = max(int(math.sqrt(limit)) + 1, 1000)
    for p in pierwsze_podstawowe:
        if p < start_segmentow:
            wszystkie_pierwsze.add(p)
    
    if limit <= start_segmentow:
        return {p for p in wszystkie_pierwsze if p <= limit}
    
    print(f"Segmentowane przesiewanie od {start_segmentow:,} do {limit:,}...")
    
    # Przetwarzaj w segmentach
    liczba_segmentow = (limit - start_segmentow + rozmiar_segmentu - 1) // rozmiar_segmentu
    przetworzone_segmenty = 0
    
    for segment_start in range(start_segmentow, limit + 1, rozmiar_segmentu):
        segment_koniec = min(segment_start + rozmiar_segmentu - 1, limit)
        
        # Przetwarzaj segment
        pierwsze_w_segmencie = segmentowane_sito_z_kolem(segment_start, segment_koniec, pierwsze_podstawowe)
        wszystkie_pierwsze.update(pierwsze_w_segmencie)
        
        przetworzone_segmenty += 1
        wyswietl_postep(przetworzone_segmenty, liczba_segmentow, "Segmenty")
    
    print(f"Segmentowane sito zakończone - znaleziono {len(wszystkie_pierwsze):,} liczb pierwszych")
    return wszystkie_pierwsze


def przetwarzaj_segment_rownolegle(args):
    """Funkcja pomocnicza do równoległego przetwarzania segmentów."""
    segment_start, segment_koniec, pierwsze_podstawowe = args
    return segmentowane_sito_z_kolem(segment_start, segment_koniec, pierwsze_podstawowe)


def segmentowane_sito_rownolegle(limit: int, rozmiar_segmentu: int = 10**6, procesy: int = None) -> Set[int]:
    """Segmentowane sito z przetwarzaniem równoległym."""
    if limit < 2:
        return set()
    
    if procesy is None:
        procesy = min(cpu_count(), 8)  # Ogranicz do 8 procesów
    
    print(f"Generowanie podstawowych liczb pierwszych...")
    pierwsze_podstawowe = generuj_podstawowe_pierwsze(limit)
    print(f"Wygenerowano {len(pierwsze_podstawowe):,} podstawowych liczb pierwszych")
    
    # Małe liczby pierwsze
    wszystkie_pierwsze = set(pierwsze_podstawowe[pierwsze_podstawowe <= int(math.sqrt(limit)) + 100])
    
    start_segmentow = max(int(math.sqrt(limit)) + 1, 1000)
    for p in pierwsze_podstawowe:
        if p < start_segmentow:
            wszystkie_pierwsze.add(p)
    
    if limit <= start_segmentow:
        return {p for p in wszystkie_pierwsze if p <= limit}
    
    print(f"Segmentowane przesiewanie równoległe ({procesy} procesów) od {start_segmentow:,} do {limit:,}...")
    
    # Przygotuj argumenty dla równoległego przetwarzania
    argumenty_segmentow = []
    for segment_start in range(start_segmentow, limit + 1, rozmiar_segmentu):
        segment_koniec = min(segment_start + rozmiar_segmentu - 1, limit)
        argumenty_segmentow.append((segment_start, segment_koniec, pierwsze_podstawowe))
    
    # Przetwarzaj segmenty równoległe z paskiem postępu
    print(f"Przetwarzanie {len(argumenty_segmentow):,} segmentów...")
    
    with Pool(processes=procesy) as pool:
        wyniki = pool.map(przetwarzaj_segment_rownolegle, argumenty_segmentow)
    
    # Połącz wyniki z paskiem postępu
    print(f"Łączenie wyników z {len(wyniki):,} segmentów...")
    for idx, pierwsze_w_segmencie in enumerate(wyniki):
        if idx % max(1, len(wyniki) // 20) == 0 or idx == len(wyniki) - 1:
            wyswietl_postep(idx + 1, len(wyniki), "  Łączenie")
        wszystkie_pierwsze.update(pierwsze_w_segmencie)
    
    print(f"Segmentowane sito równoległe zakończone - znaleziono {len(wszystkie_pierwsze):,} liczb pierwszych")
    return wszystkie_pierwsze


def sito_eratostenesa_dla_cache(limit: int, parametry: Dict[str, int] = None) -> Set[int]:
    """Zoptymalizowane Sito Eratostenesa z automatycznym wyborem algorytmu."""
    if limit < 2:
        return set()
    
    # Użyj przekazanych parametrów lub oblicz automatycznie
    if parametry is None:
        parametry = oblicz_optymalne_parametry(limit)
    
    algorytm = parametry['algorytm']
    
    # Standardowe sito
    if algorytm == 'standardowy':
        print(f"Inicjalizacja standardowego sita dla {limit:,} liczb...")
        
        # Użyj numpy boolean array dla lepszej wydajności
        sito = np.ones(limit + 1, dtype=bool)
        sito[0] = sito[1] = False
        
        print(f"Uruchamianie algorytmu sita...")
        sqrt_limit = int(math.sqrt(limit))
        
        # Optymalizuj poprzez osobne obsłużenie 2 a potem tylko liczby nieparzyste
        if limit >= 2:
            sito[4::2] = False
        
        # Liczba nieparzystych liczb do sprawdzenia
        liczby_nieparzyste = (sqrt_limit - 1) // 2
        aktualna_pozycja = 0
        
        for i in range(3, sqrt_limit + 1, 2):
            aktualna_pozycja += 1
            if aktualna_pozycja % max(1, liczby_nieparzyste // 50) == 0 or i == sqrt_limit:
                wyswietl_postep(aktualna_pozycja, liczby_nieparzyste, "  Przesiewanie")
            if sito[i]:
                sito[i*i::2*i] = False
        
        if liczby_nieparzyste > 0:
            wyswietl_postep(liczby_nieparzyste, liczby_nieparzyste, "  Przesiewanie")
        
        print(f"  Zbieranie liczb pierwszych...")
        # Użyj numpy where do szybkiego zbierania z paskiem postępu
        indices = np.where(sito)[0]
        pierwsze = set()
        for idx, p in enumerate(indices):
            if idx % max(1, len(indices) // 20) == 0 or idx == len(indices) - 1:
                wyswietl_postep(idx + 1, len(indices), "  Zbieranie")
            pierwsze.add(p)
        
        print(f"Standardowe sito zakończone - znaleziono {len(pierwsze):,} liczb pierwszych")
        return pierwsze
    
    # Segmentowane sito
    elif algorytm == 'segmentowany':
        return segmentowane_sito_duze_liczby(limit, parametry['rozmiar_segmentu'])
    
    # Równoległe segmentowane sito
    elif algorytm == 'rownolegle_segmentowany':
        return segmentowane_sito_rownolegle(limit, parametry['rozmiar_segmentu'], parametry['procesy'])
    
    else:
        # Fallback - użyj standardowego algorytmu
        print(f"Nieznany algorytm '{algorytm}', używam standardowego sita...")
        return sito_eratostenesa_dla_cache(limit, {'algorytm': 'standardowy', 'procesy': 1, 'rozmiar_segmentu': 0})


def sprawdzanie_indywidualne_dla_cache(start: int, koniec: int, pierwsze_istniejace: Set[int]) -> Set[int]:
    """Sprawdzanie pierwszości metodą indywidualną dla zakresu."""
    nowe_pierwsze = set(pierwsze_istniejace)
    
    # Dodaj małe liczby pierwsze ręcznie dla wydajności
    if koniec >= 2 and 2 not in nowe_pierwsze: nowe_pierwsze.add(2)
    if koniec >= 3 and 3 not in nowe_pierwsze: nowe_pierwsze.add(3)
    
    # Sprawdzaj tylko liczby nieparzyste zaczynając od 5
    start_nieparz = max(start, 5)
    if start_nieparz % 2 == 0:
        start_nieparz += 1
    
    if start_nieparz > koniec:
        return nowe_pierwsze
    
    liczby_do_sprawdzenia = (koniec - start_nieparz) // 2 + 1
    przetworzone = 0
    
    for i in range(start_nieparz, koniec + 1, 2):
        przetworzone += 1
        if przetworzone % max(1, liczby_do_sprawdzenia // 100) == 0 or i == koniec:
            wyswietl_postep(przetworzone, liczby_do_sprawdzenia, "  Sprawdzanie")
        if czy_pierwsza(i):
            nowe_pierwsze.add(i)
    
    return nowe_pierwsze


def wyswietl_statystyki_cache():
    """Wyświetl statystyki istniejącego cache."""
    if not os.path.exists(PLIK_CACHE_PIERWSZYCH):
        print("Plik cache nie istnieje.")
        return
    
    try:
        pierwsze, max_sprawdzone = wczytaj_istniejacy_cache()
        rozmiar_pliku = os.path.getsize(PLIK_CACHE_PIERWSZYCH)
        
        print(f"\n=== STATYSTYKI CACHE ===")
        print(f"Plik cache: {PLIK_CACHE_PIERWSZYCH}")
        print(f"Rozmiar pliku: {rozmiar_pliku:,} bajtów ({rozmiar_pliku/1024/1024:.2f} MB)")
        print(f"Maksymalna sprawdzona liczba: {max_sprawdzone:,}")
        print(f"Liczba liczb pierwszych w cache: {len(pierwsze):,}")
        if max_sprawdzone > 1:
            gestosc = len(pierwsze) / max_sprawdzone * 100
            print(f"Gęstość liczb pierwszych: {gestosc:.3f}%")
        
        # Wyświetl kilka największych liczb pierwszych
        if pierwsze:
            posortowane = sorted(pierwsze, reverse=True)[:5]
            print(f"Największe liczby pierwsze w cache: {', '.join(map(str, posortowane))}")
            
    except Exception as e:
        print(f"Błąd przy odczytywaniu cache: {e}")


def main():
    """Główna funkcja generatora cache."""
    parser = argparse.ArgumentParser(
        description="Generator cache liczb pierwszych dla spirali Ulama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s 1000000          # Generuj cache do 1 miliona (auto-optymalizacja)
  %(prog)s 100000000        # Duże liczby z automatyczną optymalizacją
  %(prog)s --statystyki     # Pokaż statystyki istniejącego cache
  %(prog)s 50000000 --procesy 4  # Wymuś 4 procesy
  %(prog)s 25000000 --segment 2000000  # Ustaw rozmiar segmentu
        """
    )
    
    parser.add_argument('limit', nargs='?', type=int,
                       help='Maksymalna liczba do sprawdzenia (domyślnie: rozszerz istniejący cache)')
    parser.add_argument('--sito', action='store_true',
                       help='Wymuś użycie Sita Eratostenesa (zalecane dla < 10M)')
    parser.add_argument('--indywidualne', action='store_true',
                       help='Wymuś sprawdzanie indywidualne')
    parser.add_argument('--rozszerz', type=int,
                       help='Rozszerz istniejący cache do podanej liczby')
    parser.add_argument('--statystyki', action='store_true',
                       help='Wyświetl statystyki istniejącego cache')
    parser.add_argument('--nadpisz', action='store_true',
                       help='Nadpisz istniejący cache zamiast go rozszerzać')
    parser.add_argument('--procesy', type=int,
                       help='Liczba procesów do przetwarzania równoległego (domyślnie: auto)')
    parser.add_argument('--segment', type=int, default=1000000,
                       help='Rozmiar segmentu dla dużych liczb (domyślnie: 1000000)')
    
    args = parser.parse_args()
    
    # Wyświetl statystyki i zakończ
    if args.statystyki:
        wyswietl_statystyki_cache()
        return
    
    # Określ limit
    if args.rozszerz:
        limit = args.rozszerz
    elif args.limit:
        limit = args.limit
    else:
        print("Błąd: Musisz podać limit lub użyć --statystyki")
        parser.print_help()
        return
    
    if limit < 2:
        print("Błąd: Limit musi być większy niż 1")
        return
    
    print(f"=== GENERATOR CACHE LICZB PIERWSZYCH ===")
    print(f"Cel: generowanie cache do {limit:,}")
    
    # Wykryj zasoby systemu i oblicz optymalne parametry
    zasoby = wykryj_zasoby_systemu()
    parametry_auto = oblicz_optymalne_parametry(limit, zasoby)
    
    # Użyj parametrów użytkownika jeśli podane, inaczej automatyczne
    parametry_finalne = {
        'algorytm': parametry_auto['algorytm'],
        'procesy': args.procesy or parametry_auto['procesy'],
        'rozmiar_segmentu': args.segment if args.segment != 1000000 else parametry_auto['rozmiar_segmentu'],
        'opis': parametry_auto['opis']
    }
    
    # Wyświetl informacje o konfiguracji
    wyswietl_konfiguracje_systemu(limit, parametry_finalne, zasoby)
    
    start_time = time.time()
    
    # Sprawdź istniejący cache
    if not args.nadpisz:
        pierwsze_istniejace, max_sprawdzone = wczytaj_istniejacy_cache()
        if max_sprawdzone >= limit:
            print(f"Cache już zawiera liczby do {max_sprawdzone:,} (>= {limit:,})")
            print("Użyj --nadpisz aby wymusić regenerację cache")
            wyswietl_statystyki_cache()
            return
        elif pierwsze_istniejace:
            print(f"Znaleziono istniejący cache z liczbami do {max_sprawdzone:,}")
            print(f"Rozszerzanie cache do {limit:,}...")
    else:
        pierwsze_istniejace, max_sprawdzone = set(), 1
        print("Generowanie nowego cache (nadpisywanie istniejącego)...")
    
    # Wybierz metodę - teraz z automatyczną optymalizacją
    if args.indywidualne:
        # Użytkownik wymusiśł sprawdzanie indywidualne
        print(f"Używanie wymuszonego sprawdzania indywidualnego...")
        start_range = 1 if args.nadpisz else max_sprawdzone + 1
        pierwsze = sprawdzanie_indywidualne_dla_cache(start_range, limit, pierwsze_istniejace)
    elif not args.nadpisz and pierwsze_istniejace and max_sprawdzone > limit * 0.7:
        # Dla rozszerzania małego zakresu użyj metody indywidualnej
        print("Dla rozszerzania małego zakresu używam metody indywidualnej...")
        pierwsze = sprawdzanie_indywidualne_dla_cache(max_sprawdzone + 1, limit, pierwsze_istniejace)
    else:
        # Użyj zoptymalizowanego sita z automatycznymi parametrami
        print(f"Używanie zoptymalizowanego sita z automatycznymi parametrami...")
        pierwsze = sito_eratostenesa_dla_cache(limit, parametry_finalne)
    
    # Zapisz cache
    print(f"Zapisywanie cache...")
    zapisz_cache(pierwsze, limit)
    
    elapsed = time.time() - start_time
    
    print(f"\n=== GENEROWANIE CACHE ZAKOŃCZONE ===")
    print(f"Czas wykonania: {elapsed:.2f} sekund")
    print(f"Wygenerowano {len(pierwsze):,} liczb pierwszych")
    print(f"Cache zapisany jako: {PLIK_CACHE_PIERWSZYCH}")
    
    # Wyświetl statystyki końcowe
    wyswietl_statystyki_cache()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"Błąd: {e}")