#!/usr/bin/env python3
"""
Eksporter Cache Liczb Pierwszych do CSV
Program eksportuje wszystkie liczby pierwsze z cache do pliku CSV.
"""

import argparse
import csv
import os
import pickle
import sys
import time
from typing import Set, List

# Nazwa domyślnego pliku cache
PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"


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


def wczytaj_cache(nazwa_pliku: str = PLIK_CACHE_PIERWSZYCH):
    """Wczytaj cache liczb pierwszych z pliku."""
    if not os.path.exists(nazwa_pliku):
        raise FileNotFoundError(f"Plik cache '{nazwa_pliku}' nie istnieje")
    
    try:
        with open(nazwa_pliku, 'rb') as f:
            dane = pickle.load(f)
        
        pierwsze = dane.get('pierwsze', set())
        max_sprawdzone = dane.get('max_sprawdzone', 0)
        
        if not isinstance(pierwsze, set):
            pierwsze = set(pierwsze) if pierwsze else set()
        
        return pierwsze, max_sprawdzone, dane
        
    except Exception as e:
        raise Exception(f"Błąd podczas wczytywania cache: {e}")


def eksportuj_do_csv_podstawowy(pierwsze: Set[int], nazwa_pliku: str):
    """Eksportuj liczby pierwsze do prostego pliku CSV (jedna kolumna)."""
    print(f"Eksportowanie do prostego CSV: {nazwa_pliku}")
    
    posortowane_pierwsze = sorted(pierwsze)
    
    try:
        with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Nagłówek
            writer.writerow(['liczba_pierwsza'])
            
            # Zapisz liczby pierwsze z paskiem postępu
            for i, liczba in enumerate(posortowane_pierwsze):
                if i % max(1, len(posortowane_pierwsze) // 100) == 0 or i == len(posortowane_pierwsze) - 1:
                    wyswietl_postep(i + 1, len(posortowane_pierwsze), "Zapisywanie CSV")
                
                writer.writerow([liczba])
        
        print(f"✅ Eksport zakończony: {nazwa_pliku}")
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas eksportu: {e}")
        return False


def eksportuj_do_csv_zaawansowany(pierwsze: Set[int], nazwa_pliku: str, chunk_size: int = 10000):
    """Eksportuj liczby pierwsze do CSV z dodatkowymi informacjami."""
    print(f"Eksportowanie do zaawansowanego CSV: {nazwa_pliku}")
    
    posortowane_pierwsze = sorted(pierwsze)
    
    try:
        with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Nagłówki
            writer.writerow([
                'indeks', 
                'liczba_pierwsza', 
                'roznica_od_poprzedniej',
                'czy_pierwsza_blizniacza',
                'chunk_id'
            ])
            
            # Zapisz liczby pierwsze z dodatkowymi informacjami
            poprzednia_pierwsza = 0
            
            for i, liczba in enumerate(posortowane_pierwsze):
                if i % max(1, len(posortowane_pierwsze) // 100) == 0 or i == len(posortowane_pierwsze) - 1:
                    wyswietl_postep(i + 1, len(posortowane_pierwsze), "Zapisywanie CSV")
                
                # Oblicz różnicę od poprzedniej liczby pierwszej
                roznica = liczba - poprzednia_pierwsza if poprzednia_pierwsza > 0 else 0
                
                # Sprawdź czy to liczba pierwsza bliźniacza (różnica 2)
                czy_blizniacza = roznica == 2
                
                # ID chunka (grupowanie po chunk_size)
                chunk_id = i // chunk_size
                
                writer.writerow([
                    i + 1,           # indeks (1-based)
                    liczba,          # liczba pierwsza
                    roznica,         # różnica od poprzedniej
                    czy_blizniacza,  # czy bliźniacza
                    chunk_id         # ID chunka
                ])
                
                poprzednia_pierwsza = liczba
        
        print(f"✅ Eksport zakończony: {nazwa_pliku}")
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas eksportu: {e}")
        return False


def eksportuj_do_csv_w_chunkach(pierwsze: Set[int], nazwa_bazowa: str, rozmiar_chunka: int = 1000000):
    """Eksportuj liczby pierwsze do wielu mniejszych plików CSV."""
    posortowane_pierwsze = sorted(pierwsze)
    
    if len(posortowane_pierwsze) <= rozmiar_chunka:
        print(f"Cache ma tylko {len(posortowane_pierwsze):,} liczb, eksportuję do jednego pliku")
        return eksportuj_do_csv_podstawowy(pierwsze, nazwa_bazowa)
    
    print(f"Eksportowanie do chunków po {rozmiar_chunka:,} liczb każdy")
    
    liczba_chunkow = (len(posortowane_pierwsze) + rozmiar_chunka - 1) // rozmiar_chunka
    
    try:
        for chunk_idx in range(liczba_chunkow):
            start = chunk_idx * rozmiar_chunka
            end = min(start + rozmiar_chunka, len(posortowane_pierwsze))
            
            chunk_pierwsze = posortowane_pierwsze[start:end]
            
            # Nazwa pliku dla chunka
            nazwa_bez_rozszerzenia = os.path.splitext(nazwa_bazowa)[0]
            rozszerzenie = os.path.splitext(nazwa_bazowa)[1] or '.csv'
            nazwa_chunka = f"{nazwa_bez_rozszerzenia}_chunk_{chunk_idx + 1:03d}{rozszerzenie}"
            
            print(f"\nChunk {chunk_idx + 1}/{liczba_chunkow}: {len(chunk_pierwsze):,} liczb -> {nazwa_chunka}")
            
            with open(nazwa_chunka, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Nagłówek
                writer.writerow(['indeks_globalny', 'liczba_pierwsza'])
                
                # Zapisz chunk
                for i, liczba in enumerate(chunk_pierwsze):
                    if i % max(1, len(chunk_pierwsze) // 20) == 0 or i == len(chunk_pierwsze) - 1:
                        wyswietl_postep(i + 1, len(chunk_pierwsze), f"Chunk {chunk_idx + 1}")
                    
                    indeks_globalny = start + i + 1
                    writer.writerow([indeks_globalny, liczba])
        
        print(f"\n✅ Eksport chunków zakończony: {liczba_chunkow} plików")
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas eksportu chunków: {e}")
        return False


def wyswietl_statystyki_csv(nazwa_pliku: str, liczba_pierwszych: int):
    """Wyświetl statystyki utworzonego pliku CSV."""
    try:
        rozmiar_pliku = os.path.getsize(nazwa_pliku)
        print(f"\n=== STATYSTYKI PLIKU CSV ===")
        print(f"Plik: {nazwa_pliku}")
        print(f"Rozmiar: {rozmiar_pliku:,} bajtów ({rozmiar_pliku/1024/1024:.2f} MB)")
        print(f"Liczb pierwszych: {liczba_pierwszych:,}")
        print(f"Średni rozmiar na liczbę: {rozmiar_pliku/liczba_pierwszych:.1f} bajtów")
    except:
        pass


def main():
    """Główna funkcja programu."""
    parser = argparse.ArgumentParser(
        description="Eksporter cache liczb pierwszych do pliku CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s                              # Prosty CSV (pierwsze.csv)
  %(prog)s --plik moje_pierwsze.csv     # Własna nazwa pliku
  %(prog)s --zaawansowany               # CSV z dodatkowymi informacjami
  %(prog)s --chunki 500000              # Podziel na chunki po 500k
  %(prog)s --cache moj_cache.pkl        # Użyj innego cache
        """
    )
    
    parser.add_argument('--plik', default='pierwsze.csv',
                       help='Nazwa pliku CSV do utworzenia (domyślnie: pierwsze.csv)')
    parser.add_argument('--cache', default=PLIK_CACHE_PIERWSZYCH,
                       help=f'Plik cache do wczytania (domyślnie: {PLIK_CACHE_PIERWSZYCH})')
    parser.add_argument('--zaawansowany', action='store_true',
                       help='Eksportuj z dodatkowymi informacjami (indeks, różnice, bliźniacze)')
    parser.add_argument('--chunki', type=int,
                       help='Podziel na chunki o podanym rozmiarze (np. 1000000)')
    parser.add_argument('--bez-statystyk', action='store_true',
                       help='Pomiń wyświetlanie statystyk')
    parser.add_argument('--nadpisz', action='store_true',
                       help='Nadpisz istniejący plik bez pytania')
    
    args = parser.parse_args()
    
    print("=== EKSPORTER CACHE LICZB PIERWSZYCH DO CSV ===")
    
    # Sprawdź czy plik docelowy już istnieje
    if not args.chunki and os.path.exists(args.plik) and not args.nadpisz:
        response = input(f"Plik '{args.plik}' już istnieje. Nadpisać? (t/n): ")
        if response.lower() != 't':
            print("Eksport anulowany.")
            return
    
    try:
        # Wczytaj cache
        print(f"Wczytywanie cache z: {args.cache}")
        pierwsze, max_sprawdzone, dane_cache = wczytaj_cache(args.cache)
        
        if not pierwsze:
            print("❌ Cache jest pusty - brak danych do eksportu")
            return
        
        print(f"Cache zawiera: {len(pierwsze):,} liczb pierwszych")
        print(f"Zakres: {min(pierwsze):,} - {max(pierwsze):,}")
        print(f"Maksymalna sprawdzona liczba: {max_sprawdzone:,}")
        
        # Eksportuj według wybranej opcji
        start_time = time.time()
        
        if args.chunki:
            sukces = eksportuj_do_csv_w_chunkach(pierwsze, args.plik, args.chunki)
        elif args.zaawansowany:
            sukces = eksportuj_do_csv_zaawansowany(pierwsze, args.plik)
        else:
            sukces = eksportuj_do_csv_podstawowy(pierwsze, args.plik)
        
        elapsed = time.time() - start_time
        print(f"\nCzas eksportu: {elapsed:.2f} sekund")
        
        # Wyświetl statystyki
        if sukces and not args.bez_statystyk and not args.chunki:
            wyswietl_statystyki_csv(args.plik, len(pierwsze))
        
        if sukces:
            print(f"\n✅ Eksport zakończony pomyślnie!")
        else:
            print(f"\n❌ Eksport nie powiódł się")
            
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"Upewnij się, że plik cache istnieje.")
    except Exception as e:
        print(f"❌ Wystąpił błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"\nNieoczekiwany błąd: {e}")