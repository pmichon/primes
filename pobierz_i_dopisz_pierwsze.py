#!/usr/bin/env python3
"""
Pobieracz i Aktualizator Cache Liczb Pierwszych
Program pobiera zbiory liczb pierwszych z t5k.org i dopisuje je do istniejącego cache.
"""

import argparse
import math
import os
import pickle
import re
import requests
import sys
import time
import zipfile
from typing import Set, List, Dict, Tuple

# Nazwa domyślnego pliku cache
PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"
KATALOG_POBRANYCH = "downloaded_primes"
BASE_URL = "https://t5k.org/lists/small/millions/"


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


def pobierz_plik(url: str, nazwa_pliku: str) -> bool:
    """Pobierz plik z podanego URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(nazwa_pliku, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            wyswietl_postep(downloaded, total_size, f"Pobieranie {os.path.basename(nazwa_pliku)}")
        
        return True
    except Exception as e:
        print(f"Błąd podczas pobierania {url}: {e}")
        return False


def wczytaj_cache(nazwa_pliku: str = PLIK_CACHE_PIERWSZYCH) -> Tuple[Set[int], int, Dict]:
    """Wczytaj istniejący cache liczb pierwszych."""
    if not os.path.exists(nazwa_pliku):
        print(f"Cache '{nazwa_pliku}' nie istnieje, utworzę nowy")
        return set(), 0, {'pierwsze': set(), 'max_sprawdzone': 0}
    
    try:
        with open(nazwa_pliku, 'rb') as f:
            dane = pickle.load(f)
        
        pierwsze = dane.get('pierwsze', set())
        max_sprawdzone = dane.get('max_sprawdzone', 0)
        
        if not isinstance(pierwsze, set):
            pierwsze = set(pierwsze) if pierwsze else set()
        
        return pierwsze, max_sprawdzone, dane
        
    except Exception as e:
        print(f"Błąd podczas wczytywania cache: {e}")
        return set(), 0, {'pierwsze': set(), 'max_sprawdzone': 0}


def zapisz_cache(pierwsze: Set[int], max_sprawdzone: int, nazwa_pliku: str = PLIK_CACHE_PIERWSZYCH):
    """Zapisz zaktualizowany cache do pliku."""
    dane = {
        'pierwsze': pierwsze,
        'max_sprawdzone': max_sprawdzone,
        'utworzony': time.strftime('%Y-%m-%d %H:%M:%S'),
        'wersja': '2.0'
    }
    
    try:
        with open(nazwa_pliku, 'wb') as f:
            pickle.dump(dane, f)
        print(f"Cache zapisano do: {nazwa_pliku}")
        return True
    except Exception as e:
        print(f"Błąd podczas zapisywania cache: {e}")
        return False


def parsuj_plik_pierwszych(sciezka_pliku: str) -> Set[int]:
    """Parsuj plik tekstowy z liczbami pierwszymi."""
    pierwsze = set()
    
    try:
        with open(sciezka_pliku, 'r') as f:
            for linia in f:
                # Pomiń nagłówki i puste linie
                if linia.strip().startswith('The First') or not linia.strip():
                    continue
                
                # Wyciągnij liczby z linii
                liczby = re.findall(r'\d+', linia)
                for liczba_str in liczby:
                    try:
                        liczba = int(liczba_str)
                        if liczba >= 2:  # Tylko liczby pierwsze >= 2
                            pierwsze.add(liczba)
                    except ValueError:
                        continue
        
        return pierwsze
        
    except Exception as e:
        print(f"Błąd podczas parsowania {sciezka_pliku}: {e}")
        return set()


def pobierz_i_przetworz_plik_pierwszych(numer_pliku: int) -> Set[int]:
    """Pobierz i przetworz jeden plik z liczbami pierwszymi."""
    nazwa_zip = f"primes{numer_pliku}.zip"
    nazwa_txt = f"primes{numer_pliku}.txt"
    url = f"{BASE_URL}{nazwa_zip}"
    
    sciezka_zip = os.path.join(KATALOG_POBRANYCH, nazwa_zip)
    sciezka_txt = os.path.join(KATALOG_POBRANYCH, nazwa_txt)
    
    # Sprawdź czy plik już istnieje
    if os.path.exists(sciezka_txt):
        print(f"Plik {nazwa_txt} już istnieje, używam istniejący")
        return parsuj_plik_pierwszych(sciezka_txt)
    
    # Pobierz plik ZIP
    print(f"Pobieranie {nazwa_zip}...")
    if not pobierz_plik(url, sciezka_zip):
        return set()
    
    # Wypakuj plik
    try:
        with zipfile.ZipFile(sciezka_zip, 'r') as zip_ref:
            zip_ref.extractall(KATALOG_POBRANYCH)
        print(f"Wypakowano {nazwa_zip}")
        
        # Usuń plik ZIP aby zaoszczędzić miejsce
        os.remove(sciezka_zip)
        
    except Exception as e:
        print(f"Błąd podczas wypakowywania {nazwa_zip}: {e}")
        return set()
    
    # Parsuj wypakowany plik
    return parsuj_plik_pierwszych(sciezka_txt)


def main():
    """Główna funkcja programu."""
    parser = argparse.ArgumentParser(
        description="Pobieracz i aktualizator cache liczb pierwszych z t5k.org",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s                        # Pobierz wszystkie 50 plików
  %(prog)s --pliki 1-5           # Pobierz pliki 1-5
  %(prog)s --pliki 1,3,5         # Pobierz pliki 1, 3 i 5
  %(prog)s --bez-aktualizacji     # Tylko pobierz, nie aktualizuj cache
  %(prog)s --cache moj_cache.pkl # Użyj innego pliku cache
        """
    )
    
    parser.add_argument('--pliki', type=str, default='1-50',
                       help='Numery plików do pobrania (np. "1-10", "1,3,5", domyślnie: "1-50")')
    parser.add_argument('--cache', default=PLIK_CACHE_PIERWSZYCH,
                       help=f'Plik cache do aktualizacji (domyślnie: {PLIK_CACHE_PIERWSZYCH})')
    parser.add_argument('--bez-aktualizacji', action='store_true',
                       help='Tylko pobierz pliki, nie aktualizuj cache')
    parser.add_argument('--wymusz-pobieranie', action='store_true',
                       help='Wymusza ponowne pobranie plików nawet jeśli już istnieją')
    parser.add_argument('--usuń-po-przetworzeniu', action='store_true',
                       help='Usuń pliki tekstowe po przetworzeniu')
    
    args = parser.parse_args()
    
    print("=== POBIERACZ I AKTUALIZATOR CACHE LICZB PIERWSZYCH ===")
    
    # Utwórz katalog na pobrane pliki
    os.makedirs(KATALOG_POBRANYCH, exist_ok=True)
    
    # Parsuj numery plików do pobrania
    numery_plików = []
    try:
        if '-' in args.pliki:
            start, end = map(int, args.pliki.split('-'))
            numery_plików = list(range(start, end + 1))
        elif ',' in args.pliki:
            numery_plików = [int(x.strip()) for x in args.pliki.split(',')]
        else:
            numery_plików = [int(args.pliki)]
    except ValueError:
        print(f"❌ Nieprawidłowy format numerów plików: {args.pliki}")
        return
    
    print(f"Pliki do pobrania: {len(numery_plików)} ({min(numery_plików)} - {max(numery_plików)})")
    
    # Wczytaj istniejący cache
    if not args.bez_aktualizacji:
        print(f"Wczytywanie cache z: {args.cache}")
        pierwsze_cache, max_sprawdzone, dane_cache = wczytaj_cache(args.cache)
        print(f"Cache zawiera: {len(pierwsze_cache):,} liczb pierwszych")
        print(f"Maksymalna sprawdzona liczba: {max_sprawdzone:,}")
    else:
        pierwsze_cache = set()
    
    # Pobierz i przetworz pliki
    wszystkie_nowe_pierwsze = set()
    start_time = time.time()
    
    for i, numer_pliku in enumerate(numery_plików):
        print(f"\n--- Przetwarzanie pliku {numer_pliku}/{max(numery_plików)} ---")
        wyswietl_postep(i, len(numery_plików), "Postęp ogólny")
        
        # Sprawdź czy wymuszać pobieranie
        if args.wymusz_pobieranie:
            nazwa_txt = f"primes{numer_pliku}.txt"
            sciezka_txt = os.path.join(KATALOG_POBRANYCH, nazwa_txt)
            if os.path.exists(sciezka_txt):
                os.remove(sciezka_txt)
        
        pierwsze_z_pliku = pobierz_i_przetworz_plik_pierwszych(numer_pliku)
        
        if pierwsze_z_pliku:
            print(f"Wczytano {len(pierwsze_z_pliku):,} liczb pierwszych z pliku {numer_pliku}")
            wszystkie_nowe_pierwsze.update(pierwsze_z_pliku)
            
            # Usuń plik tekstowy jeśli wymagane
            if args.usuń_po_przetworzeniu:
                nazwa_txt = f"primes{numer_pliku}.txt"
                sciezka_txt = os.path.join(KATALOG_POBRANYCH, nazwa_txt)
                if os.path.exists(sciezka_txt):
                    os.remove(sciezka_txt)
        else:
            print(f"❌ Nie udało się przetworzyć pliku {numer_pliku}")
    
    wyswietl_postep(len(numery_plików), len(numery_plików), "Postęp ogólny")
    
    elapsed = time.time() - start_time
    print(f"\nCzas pobierania i przetwarzania: {elapsed:.2f} sekund")
    
    # Podsumowanie pobranych danych
    if wszystkie_nowe_pierwsze:
        min_nowa = min(wszystkie_nowe_pierwsze)
        max_nowa = max(wszystkie_nowe_pierwsze)
        
        print(f"\n=== PODSUMOWANIE POBRANYCH DANYCH ===")
        print(f"Pobrano łącznie: {len(wszystkie_nowe_pierwsze):,} unikalnych liczb pierwszych")
        print(f"Zakres: {min_nowa:,} - {max_nowa:,}")
        
        # Aktualizuj cache jeśli wymagane
        if not args.bez_aktualizacji:
            print(f"\nAktualizowanie cache...")
            
            # Znajdź nowe liczby pierwsze (nie ma ich w cache)
            nowe_pierwsze = wszystkie_nowe_pierwsze - pierwsze_cache
            duplikaty = len(wszystkie_nowe_pierwsze) - len(nowe_pierwsze)
            
            if nowe_pierwsze:
                print(f"Nowych liczb pierwszych do dodania: {len(nowe_pierwsze):,}")
                if duplikaty > 0:
                    print(f"Duplikatów (już w cache): {duplikaty:,}")
                
                # Dodaj nowe liczby do cache
                pierwsze_cache.update(nowe_pierwsze)
                nowy_max = max(max_sprawdzone, max_nowa)
                
                # Zapisz zaktualizowany cache
                if zapisz_cache(pierwsze_cache, nowy_max, args.cache):
                    print(f"✅ Cache zaktualizowany!")
                    print(f"Nowa liczba pierwszych w cache: {len(pierwsze_cache):,}")
                    print(f"Nowa maksymalna sprawdzona liczba: {nowy_max:,}")
                else:
                    print(f"❌ Nie udało się zapisać cache")
            else:
                print(f"Wszystkie pobrane liczby pierwsze już są w cache")
        else:
            print(f"Cache nie został zaktualizowany (--bez-aktualizacji)")
            
        print(f"\nPliki pobrane do katalogu: {KATALOG_POBRANYCH}/")
    else:
        print(f"❌ Nie pobrano żadnych liczb pierwszych")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"\nNieoczekiwany błąd: {e}")
        import traceback
        traceback.print_exc()