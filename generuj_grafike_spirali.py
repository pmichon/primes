#!/usr/bin/env python3
"""
Generator Grafiki Spirali Ulama
Narzędzie do generowania grafiki spirali Ulama z całym cache liczb pierwszych.
Obsługuje formaty PNG i SVG.
"""

from ulam_spiral import (
    wczytaj_cache_pierwszych,
    generuj_wspolrzedne_spirali,
    generuj_svg_spirali_ulama,
    utworz_spirale_ulama,
    wizualizuj_spirale_ulama
)
import sys
import os
import argparse
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def generuj_png_spirali_ulama(wspolrzedne, pierwsze, nazwa_pliku="spirala_ulama.png", rozmiar_punktu=2.0):
    """Generuj grafiku PNG spirali Ulama z białym tłem."""
    print("\n=== GENEROWANIE GRAFIKI PNG ===")
    
    if not wspolrzedne:
        print("  Błąd: Brak współrzędnych do wygenerowania PNG")
        return ""
    
    print(f"  Przygotowywanie danych dla {len(wspolrzedne):,} punktów...")
    
    # Utwórz spiralę Ulama
    n = len(wspolrzedne)
    siatka, _, pierwsze_set = utworz_spirale_ulama(n)
    
    # Wizualizuj z białym tłem
    fig = wizualizuj_spirale_ulama(siatka, pierwsze_set, f"Spirala Ulama n={n}")
    
    # Zmień tło na białe i dostosuj kolory
    for ax in fig.get_axes():
        ax.set_facecolor('white')
        ax.set_title(ax.get_title(), color='black')
        ax.set_xlabel(ax.get_xlabel(), color='black')
        ax.set_ylabel(ax.get_ylabel(), color='black')
        ax.tick_params(colors='black')
    
    # Ustaw białe tło całego wykresu
    fig.patch.set_facecolor('white')
    
    print(f"  Zapisywanie PNG do pliku: {nazwa_pliku}")
    plt.savefig(nazwa_pliku, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    
    print(f"  ✓ Grafika PNG zapisana: {nazwa_pliku}")
    print(f"  ✓ Rozmiar pliku: {os.path.getsize(nazwa_pliku) / 1024 / 1024:.2f} MB")
    print(f"  ✓ Zawiera {len(wspolrzedne):,} punktów ({len(pierwsze):,} pierwszych)")
    
    return nazwa_pliku


def main():
    """Główna funkcja do generowania grafiki spirali Ulama."""
    parser = argparse.ArgumentParser(
        description="Generator grafiki spirali Ulama (PNG i SVG)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s                           # Interaktywny tryb (SVG)
  %(prog)s -n 1000                   # SVG z 1000 punktów
  %(prog)s -n 1000 --png             # PNG z 1000 punktów
  %(prog)s -n 1000 -f png            # PNG z 1000 punktów (alternatywna składnia)
  %(prog)s -n 1000 -o spirala.svg    # SVG z własną nazwą pliku
  %(prog)s -n 1000 --png -o spiral.png # PNG z własną nazwą pliku
        """
    )
    
    parser.add_argument('-n', '--liczba', type=int, help='Liczba punktów dla spirali')
    parser.add_argument('-f', '--format', choices=['png', 'svg'], default='svg',
                        help='Format grafiki (domyślnie: svg)')
    parser.add_argument('--png', action='store_const', const='png', dest='format',
                        help='Generuj PNG (skrót dla --format png)')
    parser.add_argument('-o', '--output', help='Nazwa pliku wyjściowego')
    parser.add_argument('-s', '--rozmiar', type=float, help='Rozmiar punktu')
    parser.add_argument('--interaktywny', action='store_true',
                        help='Wymuś tryb interaktywny')
    
    args = parser.parse_args()
    
    try:
        print(f"=== GENERATOR GRAFIKI SPIRALI ULAMA ({args.format.upper()}) ===")

        # Wczytaj cache liczb pierwszych
        print("\n[1/3] WCZYTYWANIE CACHE LICZB PIERWSZYCH")
        pierwsze_cache, max_sprawdzone = wczytaj_cache_pierwszych()

        if not pierwsze_cache:
            print("  Błąd: Brak cache liczb pierwszych!")
            print("  Uruchom najpierw 'python ulam_spiral.py' lub 'python generuj_cache_pierwszych.py'")
            return

        print(f"  ✓ Cache zawiera {len(pierwsze_cache):,} liczb pierwszych")
        print(f"  ✓ Maksymalna sprawdzona liczba: {max_sprawdzone:,}")

        # Pobierz parametry
        print(f"\n[2/3] KONFIGURACJA")
        
        # Liczba punktów
        if args.liczba:
            n = args.liczba
            if n <= 0:
                print("Błąd: Liczba punktów musi być dodatnia.")
                return
            if n > max_sprawdzone:
                print(f"Błąd: Liczba {n:,} przekracza zakres cache ({max_sprawdzone:,})")
                print("Uruchom najpierw generator cache dla większego zakresu.")
                return
        elif not args.interaktywny and len(sys.argv) == 1:
            # Tryb interaktywny gdy brak argumentów
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
        else:
            print("Błąd: Brak wymaganego parametru --liczba (-n)")
            return

        # Rozmiar punktu
        if args.rozmiar:
            rozmiar_punktu = args.rozmiar
            if rozmiar_punktu <= 0:
                print("Błąd: Rozmiar punktu musi być większy od 0.")
                return
        else:
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

        # Nazwa pliku
        if args.output:
            nazwa_pliku = args.output
        else:
            extension = 'png' if args.format == 'png' else 'svg'
            nazwa_pliku = f"spirala_ulama_n{n}.{extension}"
            
        # Sprawdź rozszerzenie
        expected_ext = '.png' if args.format == 'png' else '.svg'
        if not nazwa_pliku.endswith(expected_ext):
            nazwa_pliku += expected_ext

        print(f"\n[3/3] GENEROWANIE {args.format.upper()}")
        print(f"  Parametry:")
        print(f"    - Liczba punktów: {n:,}")
        print(f"    - Format: {args.format.upper()}")
        print(f"    - Rozmiar punktu: {rozmiar_punktu}")
        print(f"    - Nazwa pliku: {nazwa_pliku}")

        # Ostrzeżenie dla dużych plików
        if n > 100000:
            if args.interaktywny or len(sys.argv) == 1:
                odpowiedz = input(
                    f"Ostrzeżenie: n={n:,} może utworzyć bardzo duży plik. Kontynuować? (t/n): ")
                if odpowiedz.lower() != 't':
                    return
            else:
                print(f"Ostrzeżenie: n={n:,} może utworzyć bardzo duży plik.")

        # Generuj współrzędne spirali
        wspolrzedne = generuj_wspolrzedne_spirali(n)

        # Przygotuj zbiór liczb pierwszych dla tego zakresu
        pierwsze_zakres = {p for p in pierwsze_cache if p <= n}

        # Generuj grafikę w odpowiednim formacie
        if args.format == 'png':
            rezultat = generuj_png_spirali_ulama(
                wspolrzedne,
                pierwsze_zakres,
                nazwa_pliku,
                rozmiar_punktu
            )
        else:
            rezultat = generuj_svg_spirali_ulama(
                wspolrzedne,
                pierwsze_zakres,
                nazwa_pliku,
                rozmiar_punktu
            )

        if rezultat:
            print(f"\n=== GENEROWANIE {args.format.upper()} ZAKOŃCZONE ===")
            print(f"  ✓ Plik {args.format.upper()}: {rezultat}")

            # Wyświetl statystyki
            rozmiar_mb = os.path.getsize(rezultat) / 1024 / 1024
            print(f"  ✓ Rozmiar pliku: {rozmiar_mb:.2f} MB")
            print(f"  ✓ Liczby pierwsze: {len(pierwsze_zakres):,} / {n:,}")
            print(f"  ✓ Gęstość: {len(pierwsze_zakres)/n*100:.2f}%")

            if args.format == 'svg':
                print(f"\nPlik SVG można otworzyć w przeglądarce lub edytorze grafiki wektorowej.")
            else:
                print(f"\nPlik PNG można otworzyć w dowolnym edytorze grafiki.")
        else:
            print(f"  Błąd podczas generowania {args.format.upper()}")

    except KeyboardInterrupt:
        print("\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()