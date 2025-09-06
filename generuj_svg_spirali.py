#!/usr/bin/env python3
"""
Generator SVG Spirali Ulama
Narzędzie do generowania grafiki wektorowej spirali Ulama z całym cache liczb pierwszych.
"""

from ulam_spiral import (
    wczytaj_cache_pierwszych,
    generuj_wspolrzedne_spirali,
    generuj_svg_spirali_ulama
)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Główna funkcja do generowania SVG spirali Ulama z cache."""
    try:
        print("=== GENERATOR SVG SPIRALI ULAMA ===")

        # Wczytaj cache liczb pierwszych
        print("\n[1/3] WCZYTYWANIE CACHE LICZB PIERWSZYCH")
        pierwsze_cache, max_sprawdzone = wczytaj_cache_pierwszych()

        if not pierwsze_cache:
            print("  Błąd: Brak cache liczb pierwszych!")
            print("  Uruchom najpierw 'python ulam_spiral.py' lub 'python generuj_cache_pierwszych.py'")
            return

        print(f"  ✓ Cache zawiera {len(pierwsze_cache):,} liczb pierwszych")
        print(f"  ✓ Maksymalna sprawdzona liczba: {max_sprawdzone:,}")

        # Pobierz parametry od użytkownika
        print(f"\n[2/3] KONFIGURACJA")

        # Liczba punktów
        while True:
            try:
                n = int(input(f"Wprowadź liczbę punktów dla spirali (max {max_sprawdzone:,}): "))
                if n <= 0:
                    print("Proszę wprowadzić liczbę dodatnią.")
                    continue
                if n > max_sprawdzone:
                    print(f"Liczba {n:,} przekracza zakres cache ({max_sprawdzone:,})")
                    print("Uruchom najpierw generator cache dla większego zakresu.")
                    continue
                break
            except ValueError:
                print("Proszę wprowadzić poprawną liczbę całkowitą.")

        # Rozmiar punktu
        while True:
            try:
                rozmiar_str = input(f"Rozmiar punktu (domyślnie auto): ").strip()
                if not rozmiar_str:
                    # Automatyczny rozmiar na podstawie liczby punktów
                    if n <= 1000:
                        rozmiar_punktu = 3.0
                    elif n <= 10000:
                        rozmiar_punktu = 2.0
                    elif n <= 100000:
                        rozmiar_punktu = 1.5
                    else:
                        rozmiar_punktu = 1.0
                    print(f"  Automatyczny rozmiar punktu: {rozmiar_punktu}")
                    break
                else:
                    rozmiar_punktu = float(rozmiar_str)
                    if rozmiar_punktu <= 0:
                        print("Rozmiar punktu musi być większy od 0.")
                        continue
                    break
            except ValueError:
                print("Proszę wprowadzić poprawną liczbę (np. 1.5).")

        # Nazwa pliku
        nazwa_pliku = input(f"Nazwa pliku SVG (domyślnie spirala_ulama_n{n}.svg): ").strip()
        if not nazwa_pliku:
            nazwa_pliku = f"spirala_ulama_n{n}.svg"

        if not nazwa_pliku.endswith('.svg'):
            nazwa_pliku += '.svg'

        print(f"\n[3/3] GENEROWANIE SVG")
        print(f"  Parametry:")
        print(f"    - Liczba punktów: {n:,}")
        print(f"    - Rozmiar punktu: {rozmiar_punktu}")
        print(f"    - Nazwa pliku: {nazwa_pliku}")

        # Ostrzeżenie dla dużych plików
        if n > 100000:
            odpowiedz = input(
                f"Ostrzeżenie: n={n:,} może utworzyć bardzo duży plik SVG. Kontynuować? (t/n): ")
            if odpowiedz.lower() != 't':
                return

        # Generuj współrzędne spirali
        wspolrzedne = generuj_wspolrzedne_spirali(n)

        # Przygotuj zbiór liczb pierwszych dla tego zakresu
        pierwsze_zakres = {p for p in pierwsze_cache if p <= n}

        # Generuj SVG
        rezultat = generuj_svg_spirali_ulama(
            wspolrzedne,
            pierwsze_zakres,
            nazwa_pliku,
            rozmiar_punktu
        )

        if rezultat:
            print(f"\n=== GENEROWANIE SVG ZAKOŃCZONE ===")
            print(f"  ✓ Plik SVG: {rezultat}")

            # Wyświetl statystyki
            rozmiar_mb = os.path.getsize(rezultat) / 1024 / 1024
            print(f"  ✓ Rozmiar pliku: {rozmiar_mb:.2f} MB")
            print(f"  ✓ Liczby pierwsze: {len(pierwsze_zakres):,} / {n:,}")
            print(f"  ✓ Gęstość: {len(pierwsze_zakres)/n*100:.2f}%")

            print(f"\nPlik można otworzyć w przeglądarce lub edytorze grafiki wektorowej.")
        else:
            print("  Błąd podczas generowania SVG")

    except KeyboardInterrupt:
        print("\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
