#!/usr/bin/env python3
"""
Weryfikator Cache Liczb Pierwszych
Sprawdza poprawność pliku cache z liczbami pierwszymi,
weryfikuje czy wszystkie liczby są rzeczywiście pierwsze
i czy nie brakuje żadnych liczb pierwszych w zakresie.
"""

import argparse
import math
import os
import pickle
import sys
import time
from typing import Set, List, Dict, Tuple


# Nazwa pliku cache (taka sama jak w głównych skryptach)
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


def czy_pierwsza_weryfikacja(n: int) -> bool:
    """Bardzo dokładna weryfikacja pierwszości - używa trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Sprawdź wszystkie nieparzyste dzielniki do sqrt(n)
    sqrt_n = int(math.sqrt(n)) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True


def generuj_liczby_pierwsze_referencyj(limit: int) -> Set[int]:
    """Generuje liczby pierwsze metodą referencyjną (sito Eratostenesa)."""
    if limit < 2:
        return set()

    print(f"Generowanie liczb pierwszych referencyjnych do {limit:,}...")

    # Użyj prostego sita Eratostenesa jako referencji
    sito = [True] * (limit + 1)
    sito[0] = sito[1] = False

    sqrt_limit = int(math.sqrt(limit)) + 1
    for i in range(2, sqrt_limit):
        if i % max(1, sqrt_limit // 50) == 0 or i == sqrt_limit - 1:
            wyswietl_postep(i, sqrt_limit, "Generowanie ref.")
        if sito[i]:
            for j in range(i * i, limit + 1, i):
                sito[j] = False

    if sqrt_limit > 2:
        wyswietl_postep(sqrt_limit, sqrt_limit, "Generowanie ref.")

    # Zbierz liczby pierwsze
    pierwsze_ref = set()
    for i in range(2, limit + 1):
        if i % max(1, limit // 100) == 0 or i == limit:
            wyswietl_postep(i, limit, "Zbieranie ref.")
        if sito[i]:
            pierwsze_ref.add(i)

    print(f"Wygenerowano {len(pierwsze_ref):,} liczb pierwszych referencyjnych")
    return pierwsze_ref


def wczytaj_cache_do_sprawdzenia(
        nazwa_pliku: str = PLIK_CACHE_PIERWSZYCH) -> Tuple[Set[int], int, Dict]:
    """Wczytaj cache liczb pierwszych z pliku."""
    if not os.path.exists(nazwa_pliku):
        raise FileNotFoundError(f"Plik cache '{nazwa_pliku}' nie istnieje")

    try:
        with open(nazwa_pliku, 'rb') as f:
            dane = pickle.load(f)

        if not isinstance(dane, dict):
            raise ValueError("Cache nie zawiera słownika danych")

        pierwsze = dane.get('pierwsze', set())
        max_sprawdzone = dane.get('max_sprawdzone', 0)

        if not isinstance(pierwsze, set):
            pierwsze = set(pierwsze) if pierwsze else set()

        return pierwsze, max_sprawdzone, dane

    except Exception as e:
        raise Exception(f"Błąd podczas wczytywania cache: {e}")


def sprawdz_poprawnosc_pierwszosci(
        pierwsze: Set[int], max_limit: int = None) -> Dict[str, List[int]]:
    """Sprawdź czy wszystkie liczby w zbiorze są rzeczywiście pierwsze."""
    print(f"\n=== SPRAWDZANIE POPRAWNOŚCI PIERWSZOŚCI ===")

    if max_limit:
        pierwsze_do_sprawdzenia = {p for p in pierwsze if p <= max_limit}
        print(
            f"Sprawdzanie {len(pierwsze_do_sprawdzenia):,} liczb pierwszych (limit: {max_limit:,})")
    else:
        pierwsze_do_sprawdzenia = pierwsze
        print(f"Sprawdzanie wszystkich {len(pierwsze_do_sprawdzenia):,} liczb pierwszych")

    niepoprawne = []
    sprawdzone = 0

    for liczba in sorted(pierwsze_do_sprawdzenia):
        sprawdzone += 1
        if sprawdzone % max(1, len(pierwsze_do_sprawdzenia) // 100) == 0:
            wyswietl_postep(sprawdzone, len(pierwsze_do_sprawdzenia), "Weryfikacja")

        if not czy_pierwsza_weryfikacja(liczba):
            niepoprawne.append(liczba)

    wyswietl_postep(len(pierwsze_do_sprawdzenia), len(pierwsze_do_sprawdzenia), "Weryfikacja")

    return {
        'niepoprawne': niepoprawne,
        'sprawdzone': len(pierwsze_do_sprawdzenia)
    }


def sprawdz_kompletnosc(pierwsze: Set[int], max_sprawdzone: int,
                        limit_sprawdzania: int = None) -> Dict[str, List[int]]:
    """Sprawdź czy nie brakuje liczb pierwszych w zakresie."""
    print(f"\n=== SPRAWDZANIE KOMPLETNOŚCI ===")

    effective_limit = min(
        max_sprawdzone,
        limit_sprawdzania) if limit_sprawdzania else max_sprawdzone
    print(f"Sprawdzanie kompletności do {effective_limit:,}")

    if effective_limit > 10**7:
        print(
            f"Ostrzeżenie: limit {effective_limit:,} jest bardzo duży, sprawdzanie może zająć długo.")
        response = input("Kontynuować? (t/n): ")
        if response.lower() != 't':
            return {'brakujace': [], 'sprawdzony_zakres': 0}

    # Generuj liczby pierwsze metodą referencyjną
    pierwsze_ref = generuj_liczby_pierwsze_referencyj(effective_limit)

    # Znajdź brakujące liczby
    print(f"Porównywanie z cache...")
    pierwsze_w_zakresie = {p for p in pierwsze if p <= effective_limit}

    brakujace = []
    nadmiarowe = []

    # Brakujące: są w referencji, ale nie w cache
    for p in pierwsze_ref:
        if p not in pierwsze_w_zakresie:
            brakujace.append(p)

    # Nadmiarowe: są w cache, ale nie w referencji (błędne liczby pierwsze)
    for p in pierwsze_w_zakresie:
        if p not in pierwsze_ref:
            nadmiarowe.append(p)

    return {
        'brakujace': sorted(brakujace),
        'nadmiarowe': sorted(nadmiarowe),
        'sprawdzony_zakres': effective_limit,
        'cache_w_zakresie': len(pierwsze_w_zakresie),
        'referencyjne': len(pierwsze_ref)
    }


def sprawdz_strukture_cache(dane: Dict) -> Dict[str, any]:
    """Sprawdź strukturę i spójność danych w cache."""
    print(f"\n=== SPRAWDZANIE STRUKTURY CACHE ===")

    problemy = []
    ostrzezenia = []

    # Sprawdź wymagane klucze
    if 'pierwsze' not in dane:
        problemy.append("Brak klucza 'pierwsze' w cache")
    if 'max_sprawdzone' not in dane:
        problemy.append("Brak klucza 'max_sprawdzone' w cache")

    pierwsze = dane.get('pierwsze', set())
    max_sprawdzone = dane.get('max_sprawdzone', 0)

    # Sprawdź typy danych
    if not isinstance(pierwsze, (set, list)):
        problemy.append(f"'pierwsze' ma nieprawidłowy typ: {type(pierwsze)}")

    if not isinstance(max_sprawdzone, int):
        problemy.append(f"'max_sprawdzone' ma nieprawidłowy typ: {type(max_sprawdzone)}")

    # Sprawdź spójność danych
    if isinstance(pierwsze, (set, list)) and pierwsze:
        max_w_cache = max(pierwsze)
        if max_w_cache > max_sprawdzone:
            problemy.append(
                f"Największa liczba w cache ({max_w_cache:,}) > max_sprawdzone ({max_sprawdzone:,})")
        elif max_w_cache < max_sprawdzone * 0.9:  # Tolerancja 10%
            ostrzezenia.append(
                f"Największa liczba w cache ({max_w_cache:,}) znacznie mniejsza od max_sprawdzone ({max_sprawdzone:,})")

    # Sprawdź czy są liczby ujemne lub zero
    if isinstance(pierwsze, (set, list)):
        nieprawidlowe_wartosci = [p for p in pierwsze if not isinstance(p, int) or p < 2]
        if nieprawidlowe_wartosci:
            problemy.append(
                f"Znaleziono {len(nieprawidlowe_wartosci)} nieprawidłowych wartości: {nieprawidlowe_wartosci[:10]}")

    # Sprawdź duplikaty (tylko dla list)
    if isinstance(pierwsze, list):
        if len(pierwsze) != len(set(pierwsze)):
            duplikaty = len(pierwsze) - len(set(pierwsze))
            ostrzezenia.append(f"Znaleziono {duplikaty} duplikatów w liście")

    return {
        'problemy': problemy,
        'ostrzezenia': ostrzezenia,
        'pierwsze_typ': type(pierwsze).__name__,
        'pierwsze_liczba': len(pierwsze) if pierwsze else 0,
        'max_sprawdzone': max_sprawdzone,
        'max_w_cache': max(pierwsze) if pierwsze else 0
    }


def wyswietl_statystyki_cache(nazwa_pliku: str, pierwsze: Set[int], max_sprawdzone: int):
    """Wyświetl szczegółowe statystyki cache."""
    rozmiar_pliku = os.path.getsize(nazwa_pliku)

    print(f"\n=== STATYSTYKI CACHE ===")
    print(f"Plik: {nazwa_pliku}")
    print(f"Rozmiar pliku: {rozmiar_pliku:,} bajtów ({rozmiar_pliku/1024/1024:.2f} MB)")
    print(f"Maksymalna sprawdzona liczba: {max_sprawdzone:,}")
    print(f"Liczb pierwszych w cache: {len(pierwsze):,}")

    if pierwsze:
        najmniejsza = min(pierwsze)
        najwieksza = max(pierwsze)
        print(f"Zakres: {najmniejsza:,} - {najwieksza:,}")

        if max_sprawdzone > 1:
            teoretyczna_gestosc = len(pierwsze) / max_sprawdzone * 100
            print(f"Gęstość liczb pierwszych: {teoretyczna_gestosc:.3f}%")

            # Przybliżona gęstość według wzoru π(x) ≈ x / ln(x)
            if max_sprawdzone > 10:
                szacowana_liczba = max_sprawdzone / math.log(max_sprawdzone)
                print(f"Szacowana liczba (π(x) ≈ x/ln(x)): {szacowana_liczba:,.0f}")
                roznica = len(pierwsze) - szacowana_liczba
                print(
                    f"Różnica od szacowanej: {roznica:+,.0f} ({roznica/szacowana_liczba*100:+.1f}%)")


def main():
    """Główna funkcja weryfikatora cache."""
    parser = argparse.ArgumentParser(
        description="Weryfikator poprawności cache liczb pierwszych",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s                    # Sprawdź domyślny cache
  %(prog)s --plik moj_cache.pkl  # Sprawdź konkretny plik
  %(prog)s --limit 1000000    # Sprawdź tylko do 1 miliona
  %(prog)s --tylko-struktura  # Sprawdź tylko strukturę cache
  %(prog)s --bez-kompletnosci # Pomiń sprawdzanie kompletności
        """
    )

    parser.add_argument('--plik', default=PLIK_CACHE_PIERWSZYCH,
                        help=f'Plik cache do sprawdzenia (domyślnie: {PLIK_CACHE_PIERWSZYCH})')
    parser.add_argument('--limit', type=int,
                        help='Maksymalny limit sprawdzania (domyślnie: cały cache)')
    parser.add_argument('--tylko-struktura', action='store_true',
                        help='Sprawdź tylko strukturę cache, bez weryfikacji liczb')
    parser.add_argument('--bez-kompletnosci', action='store_true',
                        help='Pomiń sprawdzanie kompletności (szybsze)')
    parser.add_argument('--szczegolowe', action='store_true',
                        help='Wyświetl szczegółowe informacje o błędach')

    args = parser.parse_args()

    print(f"=== WERYFIKATOR CACHE LICZB PIERWSZYCH ===")
    print(f"Sprawdzanie pliku: {args.plik}")

    try:
        # Wczytaj cache
        print(f"\nWczytywanie cache...")
        pierwsze, max_sprawdzone, dane = wczytaj_cache_do_sprawdzenia(args.plik)

        # Wyświetl podstawowe statystyki
        wyswietl_statystyki_cache(args.plik, pierwsze, max_sprawdzone)

        # Sprawdź strukturę
        wyniki_struktury = sprawdz_strukture_cache(dane)

        if wyniki_struktury['problemy']:
            print(f"\n❌ PROBLEMY ZE STRUKTURĄ:")
            for problem in wyniki_struktury['problemy']:
                print(f"  • {problem}")
        else:
            print(f"\n✅ Struktura cache jest poprawna")

        if wyniki_struktury['ostrzezenia']:
            print(f"\n⚠️  OSTRZEŻENIA:")
            for ostrzezenie in wyniki_struktury['ostrzezenia']:
                print(f"  • {ostrzezenie}")

        # Jeśli tylko struktura, zakończ
        if args.tylko_struktura:
            return

        if not pierwsze:
            print(f"\n❌ Cache jest pusty - brak liczb pierwszych do sprawdzenia")
            return

        # Sprawdź poprawność pierwszości
        start_time = time.time()

        wyniki_poprawnosci = sprawdz_poprawnosc_pierwszosci(pierwsze, args.limit)

        if wyniki_poprawnosci['niepoprawne']:
            print(f"\n❌ ZNALEZIONO NIEPOPRAWNE LICZBY PIERWSZE:")
            print(f"Liczba błędnych liczb: {len(wyniki_poprawnosci['niepoprawne'])}")
            if args.szczegolowe:
                print(f"Błędne liczby: {wyniki_poprawnosci['niepoprawne'][:20]}")
                if len(wyniki_poprawnosci['niepoprawne']) > 20:
                    print(f"... i {len(wyniki_poprawnosci['niepoprawne']) - 20} więcej")
        else:
            print(f"\n✅ Wszystkie {wyniki_poprawnosci['sprawdzone']:,} liczb jest poprawnych")

        # Sprawdź kompletność (jeśli nie wyłączona)
        if not args.bez_kompletnosci:
            wyniki_kompletnosci = sprawdz_kompletnosc(pierwsze, max_sprawdzone, args.limit)

            if wyniki_kompletnosci.get('brakujace'):
                print(f"\n❌ BRAKUJĄCE LICZBY PIERWSZE:")
                print(f"Liczba brakujących: {len(wyniki_kompletnosci['brakujace'])}")
                if args.szczegolowe:
                    print(f"Brakujące liczby: {wyniki_kompletnosci['brakujace'][:20]}")
                    if len(wyniki_kompletnosci['brakujace']) > 20:
                        print(f"... i {len(wyniki_kompletnosci['brakujace']) - 20} więcej")
            else:
                print(f"\n✅ Cache jest kompletny w sprawdzonym zakresie")

            if wyniki_kompletnosci.get('nadmiarowe'):
                print(f"\n❌ NADMIAROWE (BŁĘDNE) LICZBY:")
                print(f"Liczba nadmiarowych: {len(wyniki_kompletnosci['nadmiarowe'])}")
                if args.szczegolowe:
                    print(f"Nadmiarowe liczby: {wyniki_kompletnosci['nadmiarowe'][:20]}")

            print(f"\nSprawdzono zakres do: {wyniki_kompletnosci['sprawdzony_zakres']:,}")
            print(f"Cache w zakresie: {wyniki_kompletnosci['cache_w_zakresie']:,}")
            print(f"Referencyjne: {wyniki_kompletnosci['referencyjne']:,}")

        elapsed = time.time() - start_time
        print(f"\n=== WERYFIKACJA ZAKOŃCZONA ===")
        print(f"Czas weryfikacji: {elapsed:.2f} sekund")

        # Podsumowanie końcowe
        wszystko_ok = (
            not wyniki_struktury['problemy'] and
            not wyniki_poprawnosci['niepoprawne'] and
            (args.bez_kompletnosci or not wyniki_kompletnosci.get('brakujace')) and
            (args.bez_kompletnosci or not wyniki_kompletnosci.get('nadmiarowe'))
        )

        if wszystko_ok:
            print(f"\n🎉 CACHE JEST POPRAWNY! ✅")
        else:
            print(f"\n⚠️  ZNALEZIONO PROBLEMY Z CACHE! ❌")

    except FileNotFoundError as e:
        print(f"\n❌ Błąd: {e}")
    except Exception as e:
        print(f"\n❌ Wystąpił błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"\nNieoczekiwany błąd: {e}")
